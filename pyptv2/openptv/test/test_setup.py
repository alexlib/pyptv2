from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os

# Paths relative to this script
LIBPATH = 'liboptv/src'
INCPATH = 'liboptv/include'

# Configure extensions
ext_modules = [
    Extension(
        name="optv.parameters",
        sources=["optv/parameters.pyx"],
        include_dirs=[np.get_include(), INCPATH],
        library_dirs=[LIBPATH],
        libraries=["optv"],
        extra_compile_args=["-O3"],
    )
]

# Just build parameters for testing
setup(
    name="optv",
    version="0.2.9",
    packages=["optv"],
    ext_modules=cythonize(ext_modules),
)
