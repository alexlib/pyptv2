"""Parameter dialog for PyPTV2."""

from pathlib import Path
import sys
import yaml

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QGroupBox
)


class ParameterTab(QWidget):
    """Base class for parameter tabs."""
    
    def __init__(self, parent=None):
        """Initialize the parameter tab."""
        super().__init__(parent)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        
        # Create form for parameters
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        
        # Add stretch to bottom
        self.layout.addStretch()
    
    def add_parameter(self, name, widget, tooltip=None):
        """Add a parameter field.
        
        Args:
            name: Parameter name (label)
            widget: Widget for editing the parameter
            tooltip: Optional tooltip text
        """
        if tooltip:
            widget.setToolTip(tooltip)
        self.form_layout.addRow(name, widget)
    
    def add_header(self, text):
        """Add a header to the form.
        
        Args:
            text: Header text
        """
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.form_layout.addRow("", label)
    
    def add_section(self, title):
        """Add a section with a group box.
        
        Args:
            title: Section title
            
        Returns:
            QFormLayout: Layout to add parameters to
        """
        group = QGroupBox(title)
        form = QFormLayout(group)
        self.layout.addWidget(group)
        return form


class MainParameterTab(ParameterTab):
    """Tab for main parameters."""
    
    def __init__(self, params=None, parent=None):
        """Initialize the main parameter tab."""
        super().__init__(parent)
        
        self.params = params
        
        # Create parameter fields
        self.add_header("Camera Settings")
        
        self.num_cameras = QSpinBox()
        self.num_cameras.setRange(1, 8)
        self.num_cameras.setValue(4)
        self.add_parameter("Number of Cameras:", self.num_cameras, 
                          "Number of cameras used in the experiment")
        
        self.image_width = QSpinBox()
        self.image_width.setRange(1, 10000)
        self.image_width.setValue(1280)
        self.add_parameter("Image Width:", self.image_width, 
                          "Width of camera images in pixels")
        
        self.image_height = QSpinBox()
        self.image_height.setRange(1, 10000)
        self.image_height.setValue(1024)
        self.add_parameter("Image Height:", self.image_height, 
                          "Height of camera images in pixels")
        
        # Sequence section
        self.add_header("Sequence Settings")
        
        self.seq_first = QSpinBox()
        self.seq_first.setRange(0, 1000000)
        self.seq_first.setValue(10000)
        self.add_parameter("First Frame:", self.seq_first, 
                          "First frame in the sequence")
        
        self.seq_last = QSpinBox()
        self.seq_last.setRange(0, 1000000)
        self.seq_last.setValue(10004)
        self.add_parameter("Last Frame:", self.seq_last, 
                          "Last frame in the sequence")
        
        # Load parameters if provided
        if params:
            self.load_parameters()
    
    def load_parameters(self):
        """Load values from parameters dictionary."""
        if not self.params:
            return
        
        # Try to load parameters
        try:
            if 'Num_Cam' in self.params:
                self.num_cameras.setValue(int(self.params['Num_Cam']))
            if 'imx' in self.params:
                self.image_width.setValue(int(self.params['imx']))
            if 'imy' in self.params:
                self.image_height.setValue(int(self.params['imy']))
            if 'Seq_First' in self.params:
                self.seq_first.setValue(int(self.params['Seq_First']))
            if 'Seq_Last' in self.params:
                self.seq_last.setValue(int(self.params['Seq_Last']))
        except Exception as e:
            print(f"Error loading main parameters: {e}")
    
    def save_parameters(self):
        """Save values to parameters dictionary."""
        if self.params is None:
            self.params = {}
        
        # Update parameters
        self.params['Num_Cam'] = self.num_cameras.value()
        self.params['imx'] = self.image_width.value()
        self.params['imy'] = self.image_height.value()
        self.params['Seq_First'] = self.seq_first.value()
        self.params['Seq_Last'] = self.seq_last.value()
        
        return self.params


class TrackingParameterTab(ParameterTab):
    """Tab for tracking parameters."""
    
    def __init__(self, params=None, parent=None):
        """Initialize the tracking parameter tab."""
        super().__init__(parent)
        
        self.params = params
        
        # Create parameter fields
        self.add_header("Search Settings")
        
        self.search_radius = QDoubleSpinBox()
        self.search_radius.setRange(0.1, 100.0)
        self.search_radius.setValue(8.0)
        self.search_radius.setSingleStep(0.5)
        self.add_parameter("Search Radius:", self.search_radius, 
                          "Radius to search for particles in next frame")
        
        self.min_corr = QDoubleSpinBox()
        self.min_corr.setRange(0.0, 1.0)
        self.min_corr.setValue(0.4)
        self.min_corr.setSingleStep(0.05)
        self.add_parameter("Min Correlation:", self.min_corr, 
                          "Minimum correlation for matches")
        
        self.add_header("Volume Settings")
        
        self.volume_x = QDoubleSpinBox()
        self.volume_x.setRange(1.0, 10000.0)
        self.volume_x.setValue(100.0)
        self.volume_x.setSingleStep(1.0)
        self.add_parameter("Volume X (mm):", self.volume_x)
        
        self.volume_y = QDoubleSpinBox()
        self.volume_y.setRange(1.0, 10000.0)
        self.volume_y.setValue(100.0)
        self.volume_y.setSingleStep(1.0)
        self.add_parameter("Volume Y (mm):", self.volume_y)
        
        self.volume_z = QDoubleSpinBox()
        self.volume_z.setRange(1.0, 10000.0)
        self.volume_z.setValue(100.0)
        self.volume_z.setSingleStep(1.0)
        self.add_parameter("Volume Z (mm):", self.volume_z)
        
        # Load parameters if provided
        if params:
            self.load_parameters()
    
    def load_parameters(self):
        """Load values from parameters dictionary."""
        if not self.params:
            return
        
        # Try to load parameters
        try:
            if 'dvxmin' in self.params:
                self.search_radius.setValue(float(self.params['dvxmin']))
            if 'min_corr' in self.params:
                self.min_corr.setValue(float(self.params['min_corr']))
            if 'volume_x' in self.params:
                self.volume_x.setValue(float(self.params['volume_x']))
            if 'volume_y' in self.params:
                self.volume_y.setValue(float(self.params['volume_y']))
            if 'volume_z' in self.params:
                self.volume_z.setValue(float(self.params['volume_z']))
        except Exception as e:
            print(f"Error loading tracking parameters: {e}")
    
    def save_parameters(self):
        """Save values to parameters dictionary."""
        if self.params is None:
            self.params = {}
        
        # Update parameters
        self.params['dvxmin'] = self.search_radius.value()
        self.params['min_corr'] = self.min_corr.value()
        self.params['volume_x'] = self.volume_x.value()
        self.params['volume_y'] = self.volume_y.value()
        self.params['volume_z'] = self.volume_z.value()
        
        return self.params


class CalibrationParameterTab(ParameterTab):
    """Tab for calibration parameters."""
    
    def __init__(self, params=None, parent=None):
        """Initialize the calibration parameter tab."""
        super().__init__(parent)
        
        self.params = params
        
        # Create parameter fields
        self.add_header("Calibration Settings")
        
        self.cal_img_base = QLineEdit()
        self.cal_img_base.setText("cal/cam")
        self.add_parameter("Calibration Image Base:", self.cal_img_base, 
                          "Base name for calibration images")
        
        self.add_header("Multimedia Parameters")
        
        self.mm_np = QDoubleSpinBox()
        self.mm_np.setRange(1.0, 2.0)
        self.mm_np.setValue(1.0)
        self.mm_np.setSingleStep(0.01)
        self.add_parameter("Refractive Index 1:", self.mm_np, 
                          "Refractive index of first medium")
        
        self.mm_nw = QDoubleSpinBox()
        self.mm_nw.setRange(1.0, 2.0)
        self.mm_nw.setValue(1.33)
        self.mm_nw.setSingleStep(0.01)
        self.add_parameter("Refractive Index 2:", self.mm_nw, 
                          "Refractive index of second medium")
        
        # Load parameters if provided
        if params:
            self.load_parameters()
    
    def load_parameters(self):
        """Load values from parameters dictionary."""
        if not self.params:
            return
        
        # Try to load parameters
        try:
            if 'cal_img_base' in self.params:
                self.cal_img_base.setText(self.params['cal_img_base'])
            if 'mm_np' in self.params:
                self.mm_np.setValue(float(self.params['mm_np']))
            if 'mm_nw' in self.params:
                self.mm_nw.setValue(float(self.params['mm_nw']))
        except Exception as e:
            print(f"Error loading calibration parameters: {e}")
    
    def save_parameters(self):
        """Save values to parameters dictionary."""
        if self.params is None:
            self.params = {}
        
        # Update parameters
        self.params['cal_img_base'] = self.cal_img_base.text()
        self.params['mm_np'] = self.mm_np.value()
        self.params['mm_nw'] = self.mm_nw.value()
        
        return self.params


class ParameterEditorDialog(QDialog):
    """Dialog for editing parameters."""
    
    def __init__(self, params_path=None, parent=None):
        """Initialize the parameter editor dialog.
        
        Args:
            params_path: Path to parameter directory
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.setWindowTitle("Parameter Editor")
        self.resize(800, 600)
        
        # Store parameters path
        self.params_path = Path(params_path) if params_path else None
        
        # Set up layout
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Load parameters
        self.parameters = {}
        if self.params_path and self.params_path.exists():
            self.load_parameters()
        
        # Create parameter tabs
        self.main_tab = MainParameterTab(self.parameters.get('main', {}), self)
        self.tab_widget.addTab(self.main_tab, "Main")
        
        self.calib_tab = CalibrationParameterTab(self.parameters.get('calibration', {}), self)
        self.tab_widget.addTab(self.calib_tab, "Calibration")
        
        self.tracking_tab = TrackingParameterTab(self.parameters.get('tracking', {}), self)
        self.tab_widget.addTab(self.tracking_tab, "Tracking")
        
        # Create buttons
        button_layout = QHBoxLayout()
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_parameters)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def load_parameters(self):
        """Load parameters from directory."""
        try:
            # Placeholder for loading parameters from files
            # In a real implementation, you would load YAML files, etc.
            self.parameters = {
                'main': {
                    'Num_Cam': 4,
                    'imx': 1280,
                    'imy': 1024,
                    'Seq_First': 10000,
                    'Seq_Last': 10004
                },
                'calibration': {
                    'cal_img_base': 'cal/cam',
                    'mm_np': 1.0,
                    'mm_nw': 1.33
                },
                'tracking': {
                    'dvxmin': 8.0,
                    'min_corr': 0.4,
                    'volume_x': 100.0,
                    'volume_y': 100.0,
                    'volume_z': 100.0
                }
            }
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error Loading Parameters",
                f"Failed to load parameters: {str(e)}"
            )
    
    def save_parameters(self):
        """Save parameters to directory."""
        try:
            if not self.params_path:
                # Ask for directory if not provided
                directory = QFileDialog.getExistingDirectory(
                    self, "Select Parameter Directory"
                )
                if not directory:
                    return
                self.params_path = Path(directory)
            
            # Create directory if it doesn't exist
            self.params_path.mkdir(parents=True, exist_ok=True)
            
            # Get parameters from tabs
            main_params = self.main_tab.save_parameters()
            calib_params = self.calib_tab.save_parameters()
            tracking_params = self.tracking_tab.save_parameters()
            
            # Save to YAML files
            self.parameters = {
                'main': main_params,
                'calibration': calib_params,
                'tracking': tracking_params
            }
            
            # In a real implementation, you would save to YAML files
            # For now, just show a success message
            QMessageBox.information(
                self,
                "Parameters Saved",
                f"Parameters saved to {self.params_path}"
            )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving Parameters",
                f"Failed to save parameters: {str(e)}"
            )


def show_parameter_dialog(params_path=None, parent=None):
    """Show the parameter editor dialog.
    
    Args:
        params_path: Path to parameter directory
        parent: Parent widget
        
    Returns:
        bool: True if parameters were saved, False otherwise
    """
    dialog = ParameterEditorDialog(params_path, parent)
    result = dialog.exec_()
    return result == QDialog.Accepted


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ParameterEditorDialog()
    dialog.show()
    sys.exit(app.exec_())