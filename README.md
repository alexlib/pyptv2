# PyPTV2

Modern Python GUI for OpenPTV (Particle Tracking Velocimetry)

## Overview

PyPTV2 is a modern reimplementation of the PyPTV GUI for the OpenPTV library. It provides a user-friendly interface for calibrating cameras, detecting particles, establishing correspondences, and tracking particles through sequences of images.

Key features:

- Modern UI based on PySide6 (Qt for Python) and Matplotlib
- Cleaner architecture with separation of UI and core functionality
- YAML-based parameter management
- Visualization of camera images, detected particles, and trajectories
- Integrated workflow for the complete PTV process

## Installation

PyPTV2 requires Python 3.8 or higher.

```bash
# Clone the repository
git clone https://github.com/alexlib/pyptv2.git
cd pyptv2

# Install in development mode
pip install -e .
```

## Usage

Launch the PyPTV2 GUI:

```bash
# Launch with the current directory as the experiment path
python -m pyptv2

# Specify an experiment directory
python -m pyptv2 /path/to/experiment
```

## Development

PyPTV2 is a work in progress. The current repository provides the modern UI framework, which will be integrated with the OpenPTV library for core functionality.

## License

PyPTV2 is released under the MIT License.

## Credits

PyPTV2 is developed by the Turbulence Structure Laboratory at Tel Aviv University, based on the original OpenPTV project.