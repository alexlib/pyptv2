#!/usr/bin/env python3
"""Setup script for PyPTV2."""

import os
from setuptools import setup, find_packages

# Read version
def get_version():
    """Read version from __version__.py."""
    with open(os.path.join('pyptv2', '__version__.py'), 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    return '0.1.0'


# Get long description from README
with open('README.md', 'r') as f:
    long_description = f.read()


# Setup configuration
setup(
    name='pyptv2',
    version=get_version(),
    description='Modern Python GUI for OpenPTV',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex Liberzon',
    author_email='alex.liberzon@gmail.com',
    url='https://github.com/alexlib/pyptv2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PySide6>=6.4.0',
        'scikit-image',
        'Pygments',
        'imagecodecs',
        'pandas',
        'tqdm',
        'matplotlib>=3.5.0',
        'scipy',
        'numpy>=1.20.0',
        'pyyaml>=6.0',
        'cython>=0.29.0'
    ],
    entry_points={
        'console_scripts': [
            'pyptv2=pyptv2.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.8',
)