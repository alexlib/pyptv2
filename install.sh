#!/bin/bash
set -e  # Exit on error

cd ./pyptv2/openptv

# Step 1: Prepare OpenPTV and convert pyx files to C
echo "Step 1: Preparing OpenPTV..."
python setup.py prepare

# Step 2: Build and install OpenPTV
echo "Step 2: Installing OpenPTV..."
python setup.py install

# Step 3: Install PyPTV2
echo "Step 3: Installing PyPTV2..."
cd ../../
python -m pip install -e .

# Step 5: Verify installation
echo "Step 5: Verifying installation..."
python -c "import pyptv2; print('Successfully imported pyptv2')"
python -c "from optv.parameters import ControlParams; print('Successfully imported optv parameters')"

echo "=== Installation completed ==="
