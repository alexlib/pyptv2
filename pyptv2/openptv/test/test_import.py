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
