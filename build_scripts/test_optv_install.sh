#\!/bin/bash
# Build and test optv installation in pixi environment
cd pyptv2/openptv
python setup.py prepare
python setup.py build_ext --inplace
python -c "import optv; print('optv imported successfully')"
cd ../..
