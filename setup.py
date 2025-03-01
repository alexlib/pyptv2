#!/usr/bin/env python3
"""Setup script for PyPTV2."""

import os
import sys
import subprocess
import numpy as np
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

# Ensure source directory for liboptv is included
LIBOPTV_SRC_DIR = os.path.join('pyptv2', 'openptv', 'liboptv', 'src')
LIBOPTV_INC_DIR = os.path.join('pyptv2', 'openptv', 'liboptv', 'include')
CYTHON_SRC_DIR = os.path.join('pyptv2', 'openptv', 'optv')

# Get the list of Cython source files
cython_sources = [
    os.path.join(CYTHON_SRC_DIR, f) 
    for f in os.listdir(CYTHON_SRC_DIR) 
    if f.endswith('.pyx')
]

# Get C source files from liboptv
c_sources = [
    os.path.join(LIBOPTV_SRC_DIR, f) 
    for f in os.listdir(LIBOPTV_SRC_DIR) 
    if f.endswith('.c')
]

# Define the extensions
extensions = []
for cython_source in cython_sources:
    module_name = os.path.splitext(os.path.basename(cython_source))[0]
    extensions.append(
        Extension(
            f'pyptv2.openptv.optv.{module_name}',
            sources=[cython_source] + c_sources,
            include_dirs=[
                LIBOPTV_INC_DIR, 
                np.get_include()
            ],
            extra_compile_args=['-O3', '-Wall'],
        )
    )

# Custom build_ext command
class BuildExt(build_ext):
    """Custom build_ext command to handle compiler options."""
    
    def build_extensions(self):
        # Check if compiler supports specific flags
        if self.compiler.compiler_type == 'unix':
            # Add more aggressive optimization
            for e in self.extensions:
                e.extra_compile_args.extend(['-O3', '-march=native'])
        
        # Build the extensions
        build_ext.build_extensions(self)


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
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': 3,
            'boundscheck': False,
            'wraparound': False,
            'initializedcheck': False,
            'nonecheck': False
        },
    ),
    cmdclass={'build_ext': BuildExt},
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