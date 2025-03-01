# PyPTV2 Development Guide

## Build, Run & Test Commands
- Install: `pip install -e .`
- Build: `python -m build`
- Run GUI: `python -m pyptv2`
- Run CLI: `python -m pyptv2 --cli`
- Run specific test: `pytest tests/test_name.py -v`

## Code Style Guidelines
- Formatting: Black with line length 88 (`black .`)
- Imports: Grouped by standard, third-party, then local imports
- Naming: snake_case for variables/functions, CamelCase for classes
- Error Handling: Use try/except blocks for specific exceptions
- Comments: Document public functions with docstrings
- Version bumping: Use `python bump_version.py --patch` for incremental updates

## UI Components
- Main Window: Central container with parameter sidebar and camera views
- Camera View: Component for displaying and interacting with camera images
- Parameter Dialog: Dialog for editing experiment parameters
- Dialogs: Specialized dialogs for calibration, detection, and tracking tasks

## Future Extensions
- Integration with OpenPTV library
- Plugin system for custom image processing, detection, and tracking algorithms
- Advanced 3D visualization of particle trajectories
- Batch processing mode for high-throughput experiments