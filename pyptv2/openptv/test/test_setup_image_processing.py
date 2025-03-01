from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os

# Paths relative to this script
LIBPATH = 'liboptv/src'
INCPATH = 'liboptv/include'

# Configure just this extension
ext_modules = [
    Extension(
        name="optv.image_processing",
        sources=["optv/image_processing.pyx"],
        include_dirs=[np.get_include(), INCPATH],
        library_dirs=[LIBPATH],
        libraries=["optv"],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="optv-image_processing",
    version="0.2.9",
    packages=["optv"],
    ext_modules=cythonize(ext_modules),
)
