#\!/bin/bash
set -e  # Exit on error

echo "=== Testing import ==="
pixi run python -c "try: 
    import pyptv2
    print('Successfully imported pyptv2')
except Exception as e:
    print('Error importing pyptv2:', e)"

