"""Setup script for the OpenPTV Python bindings (standalone version)."""

from setuptools import setup, find_packages, Extension
import numpy as np
import os
import glob

# Ensure source directory for liboptv is included
LIBOPTV_SRC_DIR = os.path.join('liboptv', 'src')
LIBOPTV_INC_DIR = os.path.join('liboptv', 'include')
INCLUDE_DIRS = [np.get_include(), '.', LIBOPTV_INC_DIR, os.path.join(LIBOPTV_INC_DIR, 'optv')]

# Get C source files
c_sources = glob.glob(os.path.join(LIBOPTV_SRC_DIR, '*.c'))

# Define a simplified extension module that includes all the C code
# This doesn't try to build the Cython extensions
extension = Extension(
    'optv._core_bindings',
    sources=[
        os.path.join(LIBOPTV_SRC_DIR, 'calibration.c'),
        os.path.join(LIBOPTV_SRC_DIR, 'parameters.c'),
        os.path.join(LIBOPTV_SRC_DIR, 'lsqadj.c'),
        os.path.join(LIBOPTV_SRC_DIR, 'trafo.c'),
        os.path.join(LIBOPTV_SRC_DIR, 'multimed.c'),
    ],
    include_dirs=INCLUDE_DIRS,
    extra_compile_args=['-O3'],
)

setup(
    name="optv",
    version="0.1.0",
    packages=['optv'],
    ext_modules=[extension],
    install_requires=[
        'numpy>=1.20.0',
        'pyyaml>=6.0',
    ],
)