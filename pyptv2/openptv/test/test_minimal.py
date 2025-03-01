try:
    print("Attempting to import parameters...")
    from optv import parameters
    print("Successfully imported parameters module")
    
    # Create a simple control parameters object
    cp = parameters.ControlParams(4)
    print("Created control parameters with", cp.get_num_cams(), "cameras")
    
except Exception as e:
    print(f"Error: {e}")
