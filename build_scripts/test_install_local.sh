#\!/bin/bash
set -e  # Exit on error

# Install from local folder
echo "=== Installing PyPTV2 from local folder ==="
pixi run pip install -e .

# Test importing
echo "=== Testing import ==="
pixi run python -c "try: import pyptv2; print('Successfully imported pyptv2'); except Exception as e: print(f'Error importing pyptv2: {e}')"

# Test running the CLI mode
echo "=== Testing CLI mode ==="
pixi run python -c "try: from pyptv2 import cli; print('Successfully imported pyptv2.cli'); except Exception as e: print(f'Error importing pyptv2.cli: {e}')"

echo "=== Installation test complete ==="
