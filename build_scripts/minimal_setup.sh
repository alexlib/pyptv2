#\!/bin/bash
# Create a minimal test with simplified setup and init

cd pyptv2/openptv

# Create a truly minimal __init__.py
cat > optv/__init__.py << 'EOT'
"""Python binding for the OpenPTV library (liboptv)."""

# Empty init to avoid circular imports during build 
EOT

# Create a modified setup.py specifically for testing
cat > test_setup.py << 'EOT'
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
EOT

# Create a minimal test script
cat > test_minimal.py << 'EOT'
try:
    print("Attempting to import parameters...")
    from optv import parameters
    print("Successfully imported parameters module")
    
    # Create a simple control parameters object
    cp = parameters.ControlParams(4)
    print("Created control parameters with", cp.get_num_cams(), "cameras")
    
except Exception as e:
    print(f"Error: {e}")
EOT

# Build the parameters module alone
python test_setup.py build_ext --inplace

# Test the parameters module
python test_minimal.py

cd ../..
