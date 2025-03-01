"""Main entry point for running PyPTV2."""

import sys
import os
from pathlib import Path
import argparse

def main():
    """Parse arguments and launch the PyPTV2 modern interface."""
    parser = argparse.ArgumentParser(description="PyPTV2 - Modern Python GUI for OpenPTV")
    parser.add_argument("path", nargs="?", help="Path to the experiment directory")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--cli", action="store_true", help="Use command line interface")
    
    args = parser.parse_args()
    
    # Handle version request
    if args.version:
        from pyptv2 import __version__
        print(f"PyPTV2 version {__version__}")
        return
    
    # Check for CLI mode
    if args.cli:
        from pyptv2 import cli
        cli()
        return
    
    # Get experiment path
    if args.path:
        exp_path = Path(args.path)
        if not exp_path.exists() or not exp_path.is_dir():
            print(f"Error: {exp_path} is not a valid directory")
            return
    else:
        exp_path = Path.cwd()
    
    print(f"Starting PyPTV2 with experiment path: {exp_path}")
    
    # Launch UI
    from pyptv2.ui.app import main as app_main
    # Set argv for GUI
    sys.argv = [sys.argv[0]]
    if args.path:
        sys.argv.append(str(exp_path))
    app_main()


if __name__ == "__main__":
    main()