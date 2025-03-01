#\!/bin/bash
# Build modules step by step to avoid circular dependencies

cd pyptv2/openptv

# Create a truly minimal __init__.py that adds modules as they're built
cat > optv/__init__.py << 'EOT'
"""Python binding for the OpenPTV library (liboptv)."""
# Empty init initially - modules will be loaded incrementally
EOT

modules=(
  "parameters"
  "calibration"
  "tracking_framebuf"
  "imgcoord"
  "image_processing"
  "orientation"
  "epipolar"
  "transforms"
  "segmentation"
  "correspondences"
  "tracker"
)

# Function to build a single module
build_module() {
  local module=$1
  echo "----------------------------------------"
  echo "Building module: $module"
  
  # Create a module-specific setup.py
  cat > test_setup_${module}.py << EOT
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
        name="optv.${module}",
        sources=["optv/${module}.pyx"],
        include_dirs=[np.get_include(), INCPATH],
        library_dirs=[LIBPATH],
        libraries=["optv"],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="optv-${module}",
    version="0.2.9",
    packages=["optv"],
    ext_modules=cythonize(ext_modules),
)
EOT

  # Build the module
  python test_setup_${module}.py build_ext --inplace
  
  # Add the module to __init__.py if successful
  if [ $? -eq 0 ]; then
    echo "from . import ${module}" >> optv/__init__.py
    echo "Module ${module} built successfully and added to __init__.py"
  else
    echo "Failed to build module ${module}"
  fi
}

# Clean up any previous builds
echo "Removing previous builds..."
find optv -name "*.c" -delete
find optv -name "*.so" -delete

# Build each module sequentially
for module in "${modules[@]}"; do
  build_module "$module"
done

# Create a test script
cat > test_all_modules.py << 'EOT'
try:
    print("Testing OpenPTV modules:")
    
    # Import optv base package
    import optv
    print("Available modules in optv:", dir(optv))
    
    # Test a few basic operations
    print("\nTesting basic functionality:")
    
    # Parameters
    from optv import parameters
    cp = parameters.ControlParams(4)
    print("- Created ControlParams with", cp.get_num_cams(), "cameras")
    
    # Tracking framebuf
    from optv import tracking_framebuf
    targ_array = tracking_framebuf.TargetArray(10)
    print("- Created TargetArray with", len(targ_array), "targets")
    
except Exception as e:
    print(f"Error: {e}")
EOT

# Test all modules
echo "----------------------------------------"
echo "Testing all built modules"
python test_all_modules.py

cd ../..
