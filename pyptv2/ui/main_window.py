"""Main window implementation for PyPTV2."""

import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from pyptv2 import __version__
from pyptv2.ui.camera_view import CameraView
from pyptv2.ui.parameter_sidebar import ParameterSidebar


class MainWindow(QMainWindow):
    """Main window for the PyPTV2 application using PySide6."""

    def __init__(self, exp_path=None, software_path=None):
        """Initialize the main window.

        Args:
            exp_path (Path, optional): Path to experiment data. Defaults to None.
            software_path (Path, optional): Path to software directory. Defaults to None.
        """
        super().__init__()
        
        # Store paths
        self.exp_path = Path(exp_path) if exp_path else Path.cwd()
        self.software_path = Path(software_path) if software_path else Path(__file__).parent.parent.parent
        
        print(f"Experiment path: {self.exp_path}")
        print(f"Software path: {self.software_path}")
        
        # Set window properties
        self.setWindowTitle(f"PyPTV2 {__version__}")
        self.resize(1200, 800)
        
        # Create the central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create the main splitter for sidebar and camera views
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Add parameter sidebar
        self.parameter_sidebar = ParameterSidebar()
        self.main_splitter.addWidget(self.parameter_sidebar)
        
        # Add camera views container
        self.camera_container = QWidget()
        self.camera_layout = QVBoxLayout(self.camera_container)
        self.main_splitter.addWidget(self.camera_container)
        
        # Set initial splitter sizes (30% sidebar, 70% cameras)
        self.main_splitter.setSizes([300, 700])
        
        # Create menus and toolbar
        self.create_menus()
        self.create_toolbar()
        
        # Initialize camera views (placeholder)
        self.camera_views = []
        
        # Show a welcome message if no experiment path is provided
        if not exp_path:
            QMessageBox.information(
                self, 
                "Welcome to PyPTV2", 
                "Please open an experiment directory to begin."
            )

    def create_menus(self):
        """Create the application menus."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        open_action = QAction("&Open Experiment...", self)
        open_action.triggered.connect(self.open_experiment)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Workflow menu
        workflow_menu = self.menuBar().addMenu("&Workflow")
        
        init_action = QAction("&Initialize", self)
        init_action.triggered.connect(self.initialize_experiment)
        workflow_menu.addAction(init_action)
        
        workflow_menu.addSeparator()
        
        calib_action = QAction("&Calibration...", self)
        calib_action.triggered.connect(self.open_calibration)
        workflow_menu.addAction(calib_action)
        
        detection_action = QAction("&Detection...", self)
        detection_action.triggered.connect(self.open_detection)
        workflow_menu.addAction(detection_action)
        
        tracking_action = QAction("&Tracking...", self)
        tracking_action.triggered.connect(self.open_tracking)
        workflow_menu.addAction(tracking_action)
        
        # Parameters menu
        params_menu = self.menuBar().addMenu("&Parameters")
        
        edit_params_action = QAction("&Edit Parameters...", self)
        edit_params_action.triggered.connect(self.edit_parameters)
        params_menu.addAction(edit_params_action)
        
        # Visualization menu
        visualization_menu = self.menuBar().addMenu("&Visualization")
        
        trajectories_action = QAction("&3D Trajectories...", self)
        trajectories_action.triggered.connect(self.open_3d_visualization)
        visualization_menu.addAction(trajectories_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        about_action = QAction("&About PyPTV2", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create the main toolbar."""
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        
        # Initialize action
        init_action = QAction("Initialize", self)
        init_action.triggered.connect(self.initialize_experiment)
        self.toolbar.addAction(init_action)
        
        self.toolbar.addSeparator()
        
        # Processing actions
        detection_action = QAction("Detect Particles", self)
        detection_action.triggered.connect(self.detect_particles)
        self.toolbar.addAction(detection_action)
        
        correspondence_action = QAction("Find Correspondences", self)
        correspondence_action.triggered.connect(self.find_correspondences)
        self.toolbar.addAction(correspondence_action)
        
        self.toolbar.addSeparator()
        
        # Tracking actions
        tracking_action = QAction("Track Sequence", self)
        tracking_action.triggered.connect(self.track_sequence)
        self.toolbar.addAction(tracking_action)
        
        show_trajectories_action = QAction("Show Trajectories", self)
        show_trajectories_action.triggered.connect(self.show_trajectories)
        self.toolbar.addAction(show_trajectories_action)
        
        # 3D visualization action
        visualization_action = QAction("3D Visualization", self)
        visualization_action.triggered.connect(self.open_3d_visualization)
        self.toolbar.addAction(visualization_action)

    def initialize_camera_views(self, num_cameras):
        """Initialize camera views based on current experiment.
        
        Args:
            num_cameras (int): Number of cameras to display
        """
        # Clear existing camera views
        for i in reversed(range(self.camera_layout.count())): 
            self.camera_layout.itemAt(i).widget().setParent(None)
        
        self.camera_views = []
        
        # Create camera grid based on number of cameras
        if num_cameras <= 2:
            # Vertical layout for 1-2 cameras
            for i in range(num_cameras):
                camera_view = CameraView(f"Camera {i+1}")
                self.camera_layout.addWidget(camera_view)
                self.camera_views.append(camera_view)
        else:
            # Grid layout for 3-4 cameras
            import math
            cols = math.ceil(math.sqrt(num_cameras))
            rows = math.ceil(num_cameras / cols)
            
            for r in range(rows):
                row_widget = QWidget()
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 0, 0, 0)
                self.camera_layout.addWidget(row_widget)
                
                for c in range(cols):
                    idx = r * cols + c
                    if idx < num_cameras:
                        camera_view = CameraView(f"Camera {idx+1}")
                        row_layout.addWidget(camera_view)
                        self.camera_views.append(camera_view)

    # Placeholder method implementations
    @Slot()
    def open_experiment(self):
        """Open an experiment directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Open Experiment Directory", str(self.exp_path)
        )
        
        if directory:
            self.exp_path = Path(directory)
            
            # Check for parameters directory
            params_dir = self.exp_path / "parameters"
            if not params_dir.is_dir():
                result = QMessageBox.question(
                    self,
                    "Parameters Missing",
                    f"No parameters directory found at {params_dir}.\nDo you want to initialize the experiment anyway?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if result == QMessageBox.No:
                    return
            
            # Initialize experiment if user confirms
            QMessageBox.information(
                self, "Experiment Loaded", f"Loaded experiment from: {self.exp_path}\nPress 'Initialize' to load parameters and images."
            )

    @Slot()
    def initialize_experiment(self):
        """Initialize the experiment."""
        QMessageBox.information(
            self, "Initialization", 
            "Experiment initialization not yet implemented in PyPTV2."
        )

    @Slot()
    def open_calibration(self):
        """Open the calibration dialog."""
        QMessageBox.information(
            self, "Calibration", 
            "Calibration dialog not yet implemented in PyPTV2."
        )

    @Slot()
    def open_detection(self):
        """Open the detection dialog."""
        QMessageBox.information(
            self, "Detection", 
            "Detection dialog not yet implemented in PyPTV2."
        )

    @Slot()
    def open_tracking(self):
        """Open the tracking dialog."""
        QMessageBox.information(
            self, "Tracking", 
            "Tracking dialog not yet implemented in PyPTV2."
        )

    @Slot()
    def edit_parameters(self):
        """Open the parameter editor dialog."""
        QMessageBox.information(
            self, "Parameter Editor", 
            "Parameter editor not yet implemented in PyPTV2."
        )

    @Slot()
    def open_3d_visualization(self):
        """Open the 3D visualization dialog."""
        QMessageBox.information(
            self, "3D Visualization", 
            "3D visualization not yet implemented in PyPTV2."
        )

    @Slot()
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About PyPTV2",
            f"<h3>PyPTV2 {__version__}</h3>"
            "<p>Modern Python GUI for OpenPTV</p>"
            "<p>Copyright © 2008-2025 Turbulence Structure Laboratory, "
            "Tel Aviv University</p>"
            "<p><a href='http://www.openptv.net'>www.openptv.net</a></p>"
        )

    @Slot()
    def detect_particles(self):
        """Detect particles in images."""
        QMessageBox.information(
            self, "Detect Particles", 
            "Particle detection not yet implemented in PyPTV2."
        )

    @Slot()
    def find_correspondences(self):
        """Find correspondences between camera views."""
        QMessageBox.information(
            self, "Find Correspondences", 
            "Correspondences not yet implemented in PyPTV2."
        )

    @Slot()
    def track_sequence(self):
        """Track particles through a sequence."""
        QMessageBox.information(
            self, "Track Sequence", 
            "Sequence tracking not yet implemented in PyPTV2."
        )

    @Slot()
    def show_trajectories(self):
        """Show particle trajectories."""
        QMessageBox.information(
            self, "Show Trajectories", 
            "Trajectory visualization not yet implemented in PyPTV2."
        )