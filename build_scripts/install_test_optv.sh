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
find optv -name "*.pyx" -exec sed -i 's/np.int_t/np.int32_t/g' {} \;

# Apply language_level directive to all pyx files
echo "Adding language_level directive to all pyx files..."
for file in optv/*.pyx; do
  if \! grep -q "# cython: language_level=3" "$file"; then
    sed -i '1s/^/# cython: language_level=3\n/' "$file"
  fi
done

for file in optv/*.pxd; do
  if \! grep -q "# cython: language_level=3" "$file"; then
    sed -i '1s/^/# cython: language_level=3\n/' "$file"
  fi
done

# Set up __init__.py to avoid circular imports
echo "Setting up __init__.py to avoid circular imports..."
cat > optv/__init__.py << 'EOT'
"""Python binding for the OpenPTV library (liboptv)."""
# Empty init to avoid circular imports during build
EOT

# Try to build parameters module first as it's the most basic
echo "Building parameters module..."
python -c "from setuptools import setup, Extension; from Cython.Build import cythonize; import numpy as np; setup(name='optv', version='0.2.9', packages=['optv'], ext_modules=cythonize([Extension('optv.parameters', ['optv/parameters.pyx'], include_dirs=[np.get_include(), 'liboptv/include'], libraries=['optv'], library_dirs=['liboptv/src'])]))"

# Test importing the parameters module
echo "Testing parameters module import..."
cd ..
python -c "import sys; sys.path.insert(0, '.'); from openptv.optv import parameters; print('Successfully imported parameters')"

cd ..
