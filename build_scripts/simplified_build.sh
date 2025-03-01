#\!/bin/bash
set -e  # Exit on error

echo "=== Building the OpenPTV library ==="
cd pyptv2/openptv

# Create a minimal vec_utils.pxd to fix the import issue
echo "Creating minimal vec_utils.pxd..."
cat > optv/vec_utils.pxd << 'EOT'
# Mimimal vec_utils.pxd with vec3d definition
cdef extern from "optv/vec_utils.h":
    ctypedef struct vec3d:
        double x
        double y
        double z

    ctypedef struct vec2d:
        double x
        double y
EOT

# Fix int_t issues
echo "Fixing int_t references in all pyx files..."
find optv -name "*.pyx" -exec sed -i 's/np\.int_t/np.int32_t/g' {} \;

# Apply language_level directive to all pyx files
echo "Adding language_level directive to all pyx files..."
for file in optv/*.pyx; do
  grep -q "# cython: language_level=3" "$file" || sed -i '1s/^/# cython: language_level=3\n/' "$file"
done

for file in optv/*.pxd; do
  grep -q "# cython: language_level=3" "$file" || sed -i '1s/^/# cython: language_level=3\n/' "$file"
done

# Set up __init__.py to avoid circular imports
echo "Setting up __init__.py to avoid circular imports..."
cat > optv/__init__.py << 'EOT'
"""Python binding for the OpenPTV library (liboptv)."""
# Empty init to avoid circular imports during build
EOT

# Create simplified setup.py for parameters module
echo "Creating simplified setup.py for parameters module..."
cat > setup_parameters.py << 'EOT'
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

ext_modules = [
    Extension(
        name="optv.parameters",
        sources=["optv/parameters.pyx"],
        include_dirs=[np.get_include(), 'liboptv/include'],
        library_dirs=['liboptv/src'],
        libraries=['optv'],
        extra_compile_args=["-O3"]
    )
]

setup(
    name="optv",
    version="0.2.9",
    packages=["optv"],
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': 3})
)
EOT

# Build parameters module
echo "Building parameters module..."
python setup_parameters.py build_ext --inplace

# Test importing the parameters module
echo "Testing parameters module import..."
cd ..
python -c "import sys; sys.path.insert(0, '.'); try: from openptv.optv import parameters; print('Successfully imported parameters'); except Exception as e: print(f'Error: {e}')"

cd ..
