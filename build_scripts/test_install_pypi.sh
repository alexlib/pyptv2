#\!/bin/bash
set -e  # Exit on error

# Install OpenPTV from PyPI
echo "=== Installing OpenPTV from PyPI ==="
pixi run pip install pyptv2

# Test importing
echo "=== Testing import ==="
pixi run python -c "try: import pyptv2; print('Successfully imported pyptv2'); except Exception as e: print(f'Error importing pyptv2: {e}')"

# Test running
echo "=== Testing CLI mode ==="
pixi run python -c "try: from pyptv2 import cli; print('Successfully imported pyptv2.cli'); except Exception as e: print(f'Error importing pyptv2.cli: {e}')"

echo "=== Installation test complete ==="
