import torch
from torch import Tensor
from typing import List, Tuple, Optional, Union, Dict

import torchvision.transforms.functional
from torchvision.transforms.functional import gaussian_blur

from hcat.lib.explore_lif import Reader
from hcat.train.transforms import _crop

import numpy as np
import skimage.io as io
import os.path

from tqdm import trange

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET


def graceful_exit(message):
    """ Decorator which returns a message upon failure"""

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = function(*args, **kwargs)
            except Exception:
                print(message)
            return result

        return wrapper

    return decorator


def calculate_indexes(pad_size: int, eval_image_size: int,
                      image_shape: int, padded_image_shape: int) -> List[List[int]]:
    """
    This calculates indexes for the complete evaluation of an arbitrarily large image by unet.
    each index is offset by eval_image_size, but has a width of eval_image_size + pad_size * 2.
    Unet needs padding on each side of the evaluation to ensure only full convolutions are used
    in generation of the final mask. If the algorithm cannot evenly create indexes for
    padded_image_shape, an additional index is added at the end of equal size.

    :param pad_size: int corresponding to the amount of padding on each side of the
                     padded image
    :param eval_image_size: int corresponding to the shape of the image to be used for
                            the final mask
    :param image_shape: int Shape of image before padding is applied
    :param padded_image_shape: int Shape of image after padding is applied

    :return: List of lists corresponding to the indexes
    """

    # We want to account for when the eval image size is super big, just return index for the whole image.
    if eval_image_size + (2 * pad_size) > image_shape:
        return [[0, image_shape - 1]]

    try:
        ind_list = torch.arange(0, image_shape, eval_image_size)
    except RuntimeError:
        raise RuntimeError(f'Calculate_indexes has incorrect values {pad_size} | {image_shape} | {eval_image_size}:\n'
                           f'You are likely trying to have a chunk smaller than the set evaluation image size. '
                           'Please decrease number of chunks.')
    ind = []
    for i, z in enumerate(ind_list):
        if i == 0:
            continue
        z1 = int(ind_list[i - 1])
        z2 = int(z - 1) + (2 * pad_size)
        if z2 < padded_image_shape:
            ind.append([z1, z2])
        else:
            break
    if not ind:  # Sometimes z is so small the first part doesnt work. Check if z_ind is empty, if it is do this!!!
        z1 = 0
        z2 = eval_image_size + pad_size * 2
        ind.append([z1, z2])
        ind.append([padded_image_shape - (eval_image_size + pad_size * 2), padded_image_shape])
    else:  # we always add at the end to ensure that the whole thing is covered.
        z1 = padded_image_shape - (eval_image_size + pad_size * 2)
        z2 = padded_image_shape - 1
        ind.append([z1, z2])
    return ind


@torch.jit.script
def crop_to_identical_size(a: torch.Tensor, b: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Crops Tensor a to the shape of Tensor b, then crops Tensor b to the shape of Tensor a.

    :param a: torch.
    :param b:
    :return:
    """
    # if a.ndim != b.ndim:
    #     raise RuntimeError('Number of dimensions of tensor "a" does not equal tensor "b".')

    if a.ndim < 3:
        raise RuntimeError('Only supports tensors with minimum 3dimmensions and shape [..., X, Y, Z]')

    a = _crop(a, x=0, y=0, z=0, w=b.shape[-3], h=b.shape[-2], d=b.shape[-1])
    b = _crop(b, x=0, y=0, z=0, w=a.shape[-3], h=a.shape[-2], d=a.shape[-1])
    return a, b


# ########################################################################################################################
# #                                                       Postprocessing
# ########################################################################################################################

# @graceful_exit('\x1b[1;31;40m' + 'ERROR: Could not remove edge cells.' + '\x1b[0m')
@torch.jit.script
def remove_edge_cells(mask: torch.Tensor) -> torch.Tensor:
    """
    Removes cells touching the border

    .. warning:
       Will not raise an error upon failure, instead returns None and prints to standard out

    :param mask: (B, X, Y, Z)
    :return: mask (B, X, Y, Z)
    """

    if mask.ndim != 4: raise RuntimeError('input.ndim != 4')

    # Mask is empty, nothing to do.
    if mask.max() == 0:
        return mask

    left = torch.unique(mask[:, 0, :, :])
    right = torch.unique(mask[:, -1, :, :])
    top = torch.unique(mask[:, :, 0, :])
    bottom = torch.unique(mask[:, :, -1, :])

    cells = torch.unique(torch.cat((left, right, top, bottom)))

    for c in cells:
        if c == 0:
            continue
        mask[mask == c] = 0

    return mask


# @graceful_exit('\x1b[1;31;40m' + 'ERROR: Could not remove improperly sized cells.' + '\x1b[0m')
@torch.jit.script
def remove_wrong_sized_cells(mask: torch.Tensor) -> torch.Tensor:
    """
    Removes cells with outlandish volumes. These have to be wrong.

    .. warning:
       Will not raise an error upon failure, instead returns None and prints to standard out

    :param mask: [B, C=1, X, Y, Z] int torch.Tensor: cell segmentation mask where each cell has a unique cell id
    :return:
    """
    unique = torch.unique(mask)
    unique = unique[unique.nonzero()]

    for u in unique:
        if (mask == u).sum() < 4000:
            mask[mask == u] = 0
        elif (mask == u).sum() > 30000:
            mask[mask == u] = 0
    return mask


# ########################################################################################################################
# #                                                       U Net Specific
# ########################################################################################################################


def pad_image_with_reflections(image: torch.Tensor, pad_size: Tuple[int] = (30, 30, 6)) -> torch.Tensor:
    """
    Pads image according to Unet spec
    expect [B, C, X, Y, Z]
    Adds pad size to each side of each dim. For example, if pad size is 10, then 10 px will be added on top, and on bottom.

    :param image:
    :param pad_size:
    :return:
    """
    if not isinstance(image, torch.Tensor):
        raise TypeError(f'Expected image to be of type torch.tensor not {type(image)}')
    for pad in pad_size:
        if pad % 2 != 0:
            raise ValueError('Padding must be divisible by 2')

    device = image.device

    image_size = image.shape
    pad_size = np.array(pad_size)

    left_pad = image.cpu().numpy()[:, :, pad_size[0] - 1::-1, :, :]
    left_pad = torch.as_tensor(left_pad.copy())
    right_pad = image.cpu().numpy()[:, :, -1:-pad_size[0] - 1:-1, :, :]
    right_pad = torch.as_tensor(right_pad.copy())
    image = torch.cat((left_pad, image.cpu(), right_pad), dim=2).to(device)

    left_pad = 0
    right_pad = 0

    bottom_pad = image.cpu().numpy()[:, :, :, pad_size[1] - 1::-1, :]
    bottom_pad = torch.as_tensor(bottom_pad.copy())
    top_pad = image.cpu().numpy()[:, :, :, -1:-pad_size[1] - 1:-1, :]
    top_pad = torch.as_tensor(top_pad.copy())
    image = torch.cat((bottom_pad, image.cpu(), top_pad), dim=3).to(device)
    bottom_pad = 0
    top_pad = 0

    bottom_pad = image.cpu().numpy()[:, :, :, :, pad_size[2] - 1::-1]
    bottom_pad = torch.as_tensor(bottom_pad.copy())
    top_pad = image.cpu().numpy()[:, :, :, :, -1:-pad_size[2] - 1:-1]
    top_pad = torch.as_tensor(top_pad.copy())

    return torch.cat((bottom_pad, image.cpu(), top_pad), dim=4).to(device)


########################################################################################################################
#                                                         Generics
########################################################################################################################

def prep_dict(data_dict, device: str):
    if isinstance(data_dict, dict):
        images = data_dict['image'].to(device).float()
        data_dict['boxes'] = data_dict['boxes']
        data_dict['labels'] = data_dict['labels']
        data_dict = [data_dict]
    elif isinstance(data_dict, list):
        images = []
        for dd in data_dict:
            images.append(dd['image'].to(device).float().squeeze(0))
        for i in range(len(data_dict)):
            data_dict[i]['boxes'] = data_dict[i]['boxes']
            data_dict[i]['labels'] = data_dict[i]['labels']
    else:
        raise RuntimeError('data_dict is neither list nor dict')

    return images, data_dict


def warn(message: str, color: str) -> None:
    c = {'green': '\x1b[1;32;40m',
         'yellow': '\x1b[1;33;40m',
         'red': '\x1b[1;31;40m',
         'norm': '\x1b[0m'}  # green, yellow, red, normal

    print(c[color.lower()] + message + c['norm'])


def get_device(verbose: Optional[bool] = False) -> str:
    if verbose: print(f'[      ] Initializing Hardware Accelerator...', end='')
    if torch.cuda.is_available():
        device = 'cuda:0'
        if verbose:
            print("\r[\x1b[1;32;40m CUDA \x1b[0m]")
    elif torch.backends.mps.is_available():
        device = 'mps'
        if verbose:
            print("\r[\x1b[1;32;40m MPS  \x1b[0m]")
    else:
        device = 'cpu'
        if verbose:
            print("\r[\x1b[1;33;40m CPU  \x1b[0m]")
            warn('WARNING: GPU not present or CUDA is not correctly initialized for GPU accelerated computation. '
                 'Analysis may be slow.', color='yellow')

    return device


def load(file: str, header_name: Optional[str] = 'TileScan 1 Merged',
         verbose: bool = False, dtype: str ='uint16', ndim: int = 3) -> Union[None, np.array]:
    """
    Loads image file (*leica or *tif) and returns an np.array

    :param file: str path to the file
    :param header_name: Optional[str] header name of lif. Does nothing image file is a tif
    :param verbose: bool print status of image loading to standard out.
    :return: np.array image matrix from file, aborts if the image is too large and returns None.
    """

    image_base = None

    if verbose:
        print(f'[      ] Loading {file}...', end='')

    if not os.path.exists(file):
        print(f'\n\x1b[1;31;40m' + f'Cannot access: \'{file}\'. No such file.' + '\x1b[0m')
        return None

    if file.endswith('.lif'):  # Load lif file
        reader = Reader(file)
        series = reader.getSeries()
        for i, header in enumerate(reader.getSeriesHeaders()):
            if header_name in header.getName():  ###'TileScan 1 Merged':

                chosen = series[i]
                for c in trange(4, desc=f'Loading LIF Image with header: {header_name}'):
                    if c == 0 and ndim == 3:
                        image_base = chosen.getXYZ(T=0, channel=c, dtype=dtype)[np.newaxis]

                        if image_base.size * 4 > 9000 * 9000 * 40 * 4:
                            print(
                                f'\x1b[1;33;40m' + f'WARNING: \'{file}\' has image size of {image_base.shape} and is very large. Analysis may fail.' + '\x1b[0m')
                            return None

                    else:
                        image_base = np.concatenate((image_base, chosen.getXYZ(T=0, channel=c)[np.newaxis]), axis=0)

            # del series, header, chosen

    elif file.endswith('.tif') or file.endswith('.png') or file.endswith('.jpg'):  # Load a tif
        image_base = io.imread(file)

        if image_base.ndim == 4:
            image_base = image_base.transpose((-1, 1, 2, 0))

        elif image_base.ndim == 3 and np.array(
                image_base.shape).min() > 4:  # Suppose you load a 3D image with one channel.
            image_base = image_base[np.newaxis, ...]
            image_base = np.concatenate((image_base, image_base, image_base, image_base), axis=0).transpose(0, 2, 3, 1)

        elif image_base.ndim == 3 and image_base.shape[-1] <= 4:  # Suppose you load a 2D image! with multiple channels

            image_base = image_base[...].transpose((2, 0, 1))  # always just take the last two channels
            # just return it...
            pass
        elif image_base.ndim == 3 and image_base.shape[0] <= 4:  # Suppose you load a 2D image! with multiple channels
            pass
        else:
            print(
                f'\x1b[1;31;40m' + f'Cannot load: \'{file}\'. Unsupported number of dimmensions: {image_base.ndim}' + '\x1b[0m')
            return None

    else:
        print(f'\x1b[1;31;40m' + f'Cannot load: \'{file}\'. Filetype not supported.' + '\x1b[0m')
        return None

    if verbose:
        print("\r[\x1b[1;32;40m DONE \x1b[0m]")
    return image_base


def rescale_box_sizes(boxes: torch.Tensor,
                      current_pixel_size: Optional[float] = None,
                      cell_diameter: Optional[int] = None,
                      ):
    scale = 1.0

    if current_pixel_size is not None:
        scale = current_pixel_size / 288.88

    elif cell_diameter is not None:
        scale = 30 / cell_diameter

    return boxes / scale


def correct_pixel_size_image(image: torch.Tensor,
                             current_pixel_size: Optional[float] = None,
                             cell_diameter: Optional[int] = None,
                             antialias: Optional[bool] = True,
                             verbose: Optional[bool] = False):
    """
    Correct an image to new pixel size...

    :param image:
    :param cell_diameter:
    :param current_pixel_size:
    :param antialias:
    :param verbose:
    :return:
    """
    if cell_diameter is None and current_pixel_size is None:
        print(f'Image was not scaled. Assuming pixel size of 288.88nm X/Y')
        return image
    else:
        if verbose:
            print(f'[      ] Scaling Image...', end='')

    if current_pixel_size is not None:
        optimal_pixel_size = 288.88
        scale = current_pixel_size / optimal_pixel_size
        c, x, y = image.shape
        new_size = [round(x * scale), round(y * scale)]

    elif cell_diameter is not None:
        scale = 30 / cell_diameter
        c, x, y = image.shape
        new_size = [round(x * scale), round(y * scale)]

    if image.min() < 0:
        image = image.div(0.5).add(0.5)
        image = torchvision.transforms.functional.resize(image, new_size, antialias=antialias).mul(0.5).add(0.5)
    else:
        image = torchvision.transforms.functional.resize(image, new_size, antialias=antialias)

    if verbose:
        print("\r[\x1b[1;32;40m DONE \x1b[0m]")

    return image


def get_dtype_offset(dtype: str = 'uint16', image_max=None) -> int:
    """ get dtype from string """

    encoding = {
        'uint16': 2 ** 16,
        'uint8': 2 ** 8,
        'uint12': 2 ** 12,
        'float64': 1,
    }
    dtype = str(dtype)

    if image_max is not None and dtype=='uint16':
        dtype = 'uint12' if 2**12 + 1 > image_max else 'uint16'

    if dtype in encoding:
        scale = encoding[dtype]

    else:
        print(
            f'\x1b[1;31;40m' + f'ERROR: Unsupported dtype: {dtype}. Currently support: {[k for k in encoding]}' + '\x1b[0m')
        scale = None
        if image_max:
            print(f'Appropriate Scale Factor inferred from image maximum: {image_max}')
            if image_max <= 256:
                scale = 256
            else:
                scale = image_max
    return scale


def cochlea_to_xml(cochlea, filename=None) -> None:
    # Xml header and root
    if filename is None:
        filename = cochlea.filename

    path = cochlea.path  # has filename appended to end
    folder = os.path.split(filename)[0]
    folder = os.path.split(folder)[-1] if len(folder) != 0 else os.path.split(os.getcwd())[1]

    _, height, width = cochlea.im_shape
    depth = 1

    root = ET.Element('annotation')
    ET.SubElement(root, 'folder').text = folder
    ET.SubElement(root, 'filename').text = filename
    ET.SubElement(root, 'path').text = path
    source = ET.SubElement(root, 'source')
    ET.SubElement(source, 'database').text = 'unknown'
    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    ET.SubElement(root, 'segmented').text = '0'

    for c in cochlea.cells:
        x0, y0, x1, y1 = c.boxes
        #  xml write xmin, xmax, ymin, ymax
        object = ET.SubElement(root, 'object')
        ET.SubElement(object, 'name').text = c.type
        ET.SubElement(object, 'pose').text = 'Unspecified'
        ET.SubElement(object, 'truncated').text = '0'
        ET.SubElement(object, 'difficult').text = '0'
        bndbox = ET.SubElement(object, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(int(x0))
        ET.SubElement(bndbox, 'ymin').text = str(int(y0))
        ET.SubElement(bndbox, 'xmax').text = str(int(x1))
        ET.SubElement(bndbox, 'ymax').text = str(int(y1))

    tree = ET.ElementTree(root)
    filename = os.path.splitext(cochlea.path)[0]
    tree.write(filename + '.xml')


def normalize_image(image: Tensor, normalize: bool, verbose: Optional[bool] = False) -> Tensor:
    if verbose and normalize:
        print(f'[      ] Normalizing to maximum brightness...', end='')
    for c in range(image.shape[0]):
        max_pixel = gaussian_blur(image[c, ...].unsqueeze(0), kernel_size=[7, 7], sigma=0.5).max()
        image[c, ...] = image[c, ...].div(max_pixel + 1e-16).clamp(0, 1) if max_pixel != 0 else image[
            c, ...]
    if verbose and normalize:
        print("\r[\x1b[1;32;40m DONE \x1b[0m]")

    return image

def make_rgb(image: Tensor) -> Tensor:
    _, x, y = image.shape
    if image.shape[0] == 2:
        image: Tensor = torch.cat((torch.zeros((1, x, y), device=image.device), image), dim=0)

    return image[0:3, ...] #ALWAYS choose


def image_to_float(image: Union[np.ndarray, Tensor], scale: int, verbose: Optional[bool] = False) -> Tensor:
    if verbose:
        print(f'[      ] Converting Image to Float... ', end='')

    if isinstance(image, np.ndarray):
        image = torch.from_numpy(image.astype(np.uint16) / scale).to(torch.float32)
    else:
        image = image.div(scale).to(torch.float32)

    if verbose:
        print("\r[\x1b[1;32;40m DONE \x1b[0m]")

    return image

def save_image_as_png(image: Tensor, filename: str, verbose: Optional[bool] = False) -> None:
    if verbose:
        print(f'[      ] Saving as {filename[:-4:]}.png...', end='')

    png = image.cpu().permute(1, 2, 0).mul(255).int().numpy().clip(0, 255).astype(np.uint8)
    io.imsave(filename[:-4:] + '.png', png[:, :, [2, 0, 1]])
    io.imsave(filename[:-4:] + '_scaled.tif', png[:, :, [2, 0, 1]])

    del png
    if verbose:
        print("\r[\x1b[1;32;40m DONE \x1b[0m]")


########################################################################################################################
#                                                         Plotting
########################################################################################################################

def plot_embedding(embedding: torch.Tensor, centroids: torch.Tensor) -> None:
    num = 25
    x = embedding.detach().cpu().numpy()[0, 0, ...].flatten() * num
    y = embedding.detach().cpu().numpy()[0, 1, ...].flatten() * num
    plt.hist2d(y, x, bins=(embedding.shape[2], embedding.shape[3]))
    print(centroids)
    plt.plot(centroids[0, :, 1].cpu().numpy(), centroids[0, :, 0].cpu().numpy(), 'ro')

    plt.show()

def make_embedding_image(embedding):
    x = embedding.detach().cpu().numpy()[0, 0, ...].flatten()
    y = embedding.detach().cpu().numpy()[0, 1, ...].flatten()
    histogram,_,_ = np.histogram2d(x, y, bins=(embedding.shape[2], embedding.shape[3]))
    return torch.from_numpy(histogram)



if __name__ == "__main__":
    cochlea = torch.load('test.cochlea')
    cochlea_to_xml(cochlea)
