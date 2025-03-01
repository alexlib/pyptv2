#\!/bin/bash
# Fix segmentation.pyx issue and try to build again

cd pyptv2/openptv

# Fix int_t issue in segmentation.pyx
sed -i 's/ctypedef np.int_t DTYPE_t/ctypedef np.int32_t DTYPE_t/' optv/segmentation.pyx

# Try building again
python setup.py prepare
python setup.py build_ext --inplace

# Test import
python -c "try: import optv; print('optv imported successfully'); except Exception as e: print(f'Error importing optv: {e}')"

cd ../..
