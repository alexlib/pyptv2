#\!/bin/bash
# Fix all numpy int_t references in multiple files

cd pyptv2/openptv

# Fix all numpy int_t references in pyx files
for file in optv/*.pyx; do
  echo "Fixing $file..."
  sed -i 's/np.int_t/np.int32_t/g' $file
done

# Create a simple test module 
mkdir -p test_build
cat > test_build/simple_test.py << 'EOT'
import numpy as np
import sys
import os

# Add optv to the path
sys.path.insert(0, os.path.abspath('..'))

try:
    print("NumPy version:", np.__version__)
    
    # Try importing with modified imports
    print("Attempting to import optv.parameters...")
    from optv import parameters
    print("Successfully imported parameters")
    
    print("\nTesting parameters module:")
    # Create a simple control parameters object
    cp = parameters.ControlParams(4)
    print("Created control parameters with", cp.get_num_cams(), "cameras")
    
except Exception as e:
    print(f"Error: {e}")
EOT

# Fix the __init__.py to avoid circular imports
cat > optv/__init__.py.new << 'EOT'
"""Python binding for the OpenPTV library (liboptv).

This package provides Python bindings to the C implementation of the OpenPTV
algorithms for 3D particle tracking velocimetry.
"""

from . import parameters

# Delay other imports to avoid circular imports
__all__ = [
    'parameters',
    'calibration',
    'correspondences',
    'epipolar',
    'image_processing',
    'imgcoord',
    'orientation',
    'segmentation',
    'tracker',
    'tracking_framebuf',
    'transforms',
]

# Import the rest after parameters
from . import calibration
from . import correspondences
from . import epipolar
from . import image_processing
from . import imgcoord
from . import orientation
from . import segmentation
from . import tracker
from . import tracking_framebuf
from . import transforms
EOT

# Backup the original
cp optv/__init__.py optv/__init__.py.bak
mv optv/__init__.py.new optv/__init__.py

# Run prepare with fixed files
python setup.py prepare

# Test single module import
cd test_build
python simple_test.py

cd ../..
