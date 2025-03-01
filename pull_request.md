# Fix OpenPTV Cython build and import issues

## Summary
- Fixed compatibility issues with Python 3.12 and Cython 3.0
- Updated the build system for OpenPTV Cython extensions
- Added proper module import handling in bridge.py
- Excluded build artifacts from Git

## Changes
1. Fixed numpy array handling in parameters.pyx with numpy.set_array_base()
2. Updated function pointer types in transforms.pyx for Cython 3.0
3. Modified transforms.pxd to use nogil specifier for C functions
4. Removed vec_utils import since it's not a compiled module
5. Updated bridge.py to handle direct importing of optv modules when in the import path
6. Added setup.py, pyproject.toml and requirements.txt for OpenPTV
7. Added standalone setup_optv.py for simplified installation
8. Updated .gitignore to exclude generated C files and build artifacts

## Testing
Successfully built and ran the Cython extensions with Python 3.12. All tests pass, and the main application launches correctly.

