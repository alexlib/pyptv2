# Python 3.11+ Compatibility Updates

This branch contains updates to make PyPTV2 compatible with Python 3.11+, focusing on the following changes:

## Key Changes
1. **Cython Compatibility**:
   - Added language_level directives to Cython files
   - Fixed NumPy type declarations (replaced `np.int64_t` with `np.int32_t`)
   - Created minimal `vec_utils.pxd` implementation for vec3d/vec2d structs
   - Added `set_array_base()` for NumPy array handling in Python 3.12+

2. **Build System Improvements**:
   - Added Pixi configuration for reproducible environments
   - Created build scripts for step-by-step compilation
   - Fixed circular import issues in OpenPTV modules

3. **Test Utilities**:
   - Added test scripts to verify module loading
   - Created debugging utilities for isolated module builds

## Using Pixi Environment
```bash
# Install pixi if you don't have it
curl -fsSL https://pixi.sh/install.sh | bash

# Create the environment and activate it
pixi install
pixi shell

# Install pyptv2 in development mode
pip install -e .

# Verify installation
python -c "import pyptv2; print('PyPTV2 imported successfully')"
```

## Known Issues
- The OpenPTV Cython modules still require fixes for full Python 3.11+ compatibility
- The bridge module handles import errors gracefully but provides warnings
- NumPy array ownership and typing issues need to be fixed in parameters.pyx
