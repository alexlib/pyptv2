try:
    print("Testing OpenPTV modules:")
    
    # Import optv base package
    import optv
    print("Available modules in optv:", dir(optv))
    
    # Test a few basic operations
    print("\nTesting basic functionality:")
    
    # Parameters
    from optv import parameters
    cp = parameters.ControlParams(4)
    print("- Created ControlParams with", cp.get_num_cams(), "cameras")
    
    # Tracking framebuf
    from optv import tracking_framebuf
    targ_array = tracking_framebuf.TargetArray(10)
    print("- Created TargetArray with", len(targ_array), "targets")
    
except Exception as e:
    print(f"Error: {e}")
