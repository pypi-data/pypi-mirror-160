import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    description="A Hair Cell Analysis Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    entry_points={'console_scripts': ['hcat-segment=hcat.main:segment',
                                      'hcat-detect=hcat.main:detect',
                                      'hcat=hcat.main:cli']},
    install_requires=[
        'auto_mix_prep>=0.2.0',
        'click>=8.1.3',
        'elasticdeform>=0.4.9',
        'GPy>=1.10.0',
        'kornia>=0.6.5',
        'lz4>=4.0.1',
        'matplotlib>=3.5.1',
        'numpy>=1.22.3',
        'pandas>=1.4.2',
        'Pillow>=9.2.0',
        'psutil>=5.9.1',
        'PySimpleGUI>=4.60.1',
        'scikit_image>=0.19.2',
        'scikit_learn>=1.1.1',
        'scipy>=1.7.3',
        'setuptools>=61.2.0',
        'timm>=0.5.4',
        'torch>=1.12.0',
        'torchvision>=0.13.0',
        'tqdm>=4.64.0',
        'wget>=3.2',
    ]
)
