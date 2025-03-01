#\!/bin/bash
# Fix numpy int types in multiple files

cd pyptv2/openptv

# Fix int_t in segmentation.pyx
sed -i 's/ctypedef np.int_t DTYPE_t/ctypedef np.int32_t DTYPE_t/' optv/segmentation.pyx

# Fix int_t in orientation.pyx
sed -i 's/np.ndarray\[ndim=1, dtype=np.int_t\] used/np.ndarray\[ndim=1, dtype=np.int32_t\] used/' optv/orientation.pyx

# Create a simplified test file
cat > test_import.py << 'EOT'
try:
    import numpy as np
    print("NumPy version:", np.__version__)
    
    # Try importing one module that doesn't require the others
    try:
        from optv import parameters
        print("Successfully imported parameters module")
    except ImportError as e:
        print(f"Error importing parameters: {e}")
    
    # Try importing the full package
    try:
        import optv
        print("Successfully imported optv package")
        print("Available modules:", dir(optv))
    except ImportError as e:
        print(f"Error importing optv: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
EOT

# Test building with prepare
python setup.py prepare

# Test importing
python test_import.py

cd ../..
