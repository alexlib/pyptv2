"""Command-line interface for PyPTV2."""

import argparse
from pathlib import Path

def cli():
    """Run the PyPTV2 command-line interface."""
    parser = argparse.ArgumentParser(description="PyPTV2 CLI")
    parser.add_argument("command", choices=["calibrate", "detect", "track", "visualize"],
                        help="Command to execute")
    parser.add_argument("path", help="Path to the experiment directory")
    parser.add_argument("--config", "-c", help="Path to custom configuration file")
    parser.add_argument("--output", "-o", help="Output directory")
    
    args = parser.parse_args()
    
    # Get experiment path
    exp_path = Path(args.path)
    if not exp_path.exists() or not exp_path.is_dir():
        print(f"Error: {exp_path} is not a valid directory")
        return
    
    # Execute the requested command
    if args.command == "calibrate":
        print(f"Running calibration for experiment: {exp_path}")
        # TODO: Implement calibration
    
    elif args.command == "detect":
        print(f"Running particle detection for experiment: {exp_path}")
        # TODO: Implement detection
    
    elif args.command == "track":
        print(f"Running tracking for experiment: {exp_path}")
        # TODO: Implement tracking
    
    elif args.command == "visualize":
        print(f"Visualizing results for experiment: {exp_path}")
        # TODO: Implement visualization
    
    return "CLI execution completed"


if __name__ == "__main__":
    cli()