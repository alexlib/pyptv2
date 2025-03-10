"""Parameter sidebar for the PyPTV2 UI."""

from pathlib import Path
import os
import json

from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
    QPushButton,
    QToolBar,
    QMenu,
    QDialog,
    QFileDialog,
    QMessageBox,
    QSplitter,
    QSpinBox,
    QCheckBox,
    QLineEdit,
    QTextEdit,
    QDoubleSpinBox,
    QComboBox
)


class ParameterDialog(QDialog):
    """Base dialog for editing parameters."""
    
    def __init__(self, title="Edit Parameters", parent=None):
        """Initialize the parameter dialog.
        
        Args:
            title: Dialog title
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)
        
        # Create layout
        self.main_layout = QVBoxLayout(self)
        
        # Parameter container
        self.param_container = QWidget()
        self.param_layout = QFormLayout(self.param_container)
        self.main_layout.addWidget(self.param_container)
        
        # Add buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Apply")
        self.save_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(button_layout)
        
    def add_parameter(self, name, widget, tooltip=None):
        """Add a parameter field to the dialog.
        
        Args:
            name: Parameter name (label)
            widget: Widget for editing the parameter
            tooltip: Optional tooltip text
        """
        if tooltip:
            widget.setToolTip(tooltip)
        self.param_layout.addRow(name, widget)
        
    def add_header(self, text):
        """Add a header to the parameter form.
        
        Args:
            text: Header text
        """
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.param_layout.addRow("", label)


class MainParameterDialog(ParameterDialog):
    """Dialog for editing main parameters."""
    
    def __init__(self, params=None, parent=None):
        """Initialize the main parameter dialog.
        
        Args:
            params: Main parameters object
            parent: Parent widget
        """
        super().__init__("Main Parameters", parent)
        
        self.params = params
        
        # Create parameter fields
        # Camera section
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


class ParameterSet:
    """Class to represent a parameter set."""
    
    def __init__(self, name, path):
        """Initialize a parameter set.
        
        Args:
            name: Parameter set name
            path: Path to parameter files
        """
        self.name = name
        self.path = Path(path) if isinstance(path, str) else path
        self.is_active = False
        
        # Load parameters from files (placeholder)
        self.main_params = {}
        self.calib_params = {}
        self.tracking_params = {}
        self._create_default_params()
    
    def _create_default_params(self):
        """Create default parameter placeholders."""
        self.main_params = {
            "Num_Cam": 4,
            "imx": 1280,
            "imy": 1024,
            "Seq_First": 10000,
            "Seq_Last": 10004
        }
        
        self.calib_params = {
            "calibration": "sample"
        }
        
        self.tracking_params = {
            "tracking": "sample"
        }
        
        self.sequence_params = {
            "Seq_First": 10000,
            "Seq_Last": 10004
        }


class ParameterSidebar(QWidget):
    """Widget for displaying and managing parameters."""
    
    # Signals
    parameter_set_changed = Signal(object)  # ParameterSet object
    
    def __init__(self, parent=None):
        """Initialize the parameter sidebar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 0)
        
        header_label = QLabel("Parameters")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))
        
        self.add_action = QAction("Add", self)
        self.add_action.triggered.connect(self._add_parameter_set)
        self.toolbar.addAction(self.add_action)
        
        self.toolbar.addSeparator()
        
        self.refresh_action = QAction("Refresh", self)
        self.refresh_action.triggered.connect(self._refresh_parameters)
        self.toolbar.addAction(self.refresh_action)
        
        layout.addWidget(self.toolbar)
        
        # Create tree widget for parameters
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.tree_widget)
        
        # Initialize parameter sets
        self.parameter_sets = []
        self.active_parameter_set = None
        
        # Add sample parameter sets
        self._add_sample_parameter_sets()
    
    def _add_sample_parameter_sets(self):
        """Add sample parameter sets for demonstration."""
        # Add a few sample parameter sets
        self.add_parameter_set(ParameterSet("Default", "./parameters"))
        self.add_parameter_set(ParameterSet("Run1", "./parametersRun1"))
        
        # Set the first one as active
        if self.parameter_sets:
            self.set_active_parameter_set(self.parameter_sets[0])
    
    def add_parameter_set(self, parameter_set):
        """Add a parameter set to the sidebar.
        
        Args:
            parameter_set: ParameterSet object
        """
        self.parameter_sets.append(parameter_set)
        
        # Create top level item for the parameter set
        item = QTreeWidgetItem(self.tree_widget)
        item.setText(0, parameter_set.name)
        item.setData(0, Qt.UserRole, parameter_set)
        
        # If active, make bold
        if parameter_set.is_active:
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
        
        # Add subitems for parameter types
        main_params_item = QTreeWidgetItem(item)
        main_params_item.setText(0, "Main Parameters")
        main_params_item.setData(0, Qt.UserRole, "main")
        
        calib_params_item = QTreeWidgetItem(item)
        calib_params_item.setText(0, "Calibration Parameters")
        calib_params_item.setData(0, Qt.UserRole, "calib")
        
        tracking_params_item = QTreeWidgetItem(item)
        tracking_params_item.setText(0, "Tracking Parameters")
        tracking_params_item.setData(0, Qt.UserRole, "tracking")
        
        self.tree_widget.expandItem(item)
    
    def set_active_parameter_set(self, parameter_set):
        """Set a parameter set as active.
        
        Args:
            parameter_set: ParameterSet object
        """
        # Update active status
        for ps in self.parameter_sets:
            ps.is_active = (ps == parameter_set)
        
        self.active_parameter_set = parameter_set
        
        # Update tree widget
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            ps = item.data(0, Qt.UserRole)
            
            font = item.font(0)
            font.setBold(ps.is_active)
            item.setFont(0, font)
        
        # Emit signal
        self.parameter_set_changed.emit(parameter_set)
    
    def _show_context_menu(self, position):
        """Show context menu for tree items.
        
        Args:
            position: Menu position
        """
        item = self.tree_widget.itemAt(position)
        if not item:
            return
        
        # Create menu
        menu = QMenu()
        
        # Get item data
        parent_item = item.parent()
        
        if parent_item is None:
            # Top level item (parameter set)
            parameter_set = item.data(0, Qt.UserRole)
            
            set_active_action = QAction("Set as Active", self)
            set_active_action.triggered.connect(
                lambda: self.set_active_parameter_set(parameter_set)
            )
            menu.addAction(set_active_action)
            
            menu.addSeparator()
            
            copy_action = QAction("Copy", self)
            copy_action.triggered.connect(
                lambda: self._copy_parameter_set(parameter_set)
            )
            menu.addAction(copy_action)
            
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(
                lambda: self._delete_parameter_set(parameter_set)
            )
            menu.addAction(delete_action)
        else:
            # Parameter type item
            parameter_set = parent_item.data(0, Qt.UserRole)
            parameter_type = item.data(0, Qt.UserRole)
            
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(
                lambda: self._edit_parameters(parameter_set, parameter_type)
            )
            menu.addAction(edit_action)
        
        # Show menu
        menu.exec_(self.tree_widget.viewport().mapToGlobal(position))
    
    def _add_parameter_set(self):
        """Add a new parameter set."""
        # Open directory dialog
        directory = QFileDialog.getExistingDirectory(
            self, "Select Parameter Directory"
        )
        
        if directory:
            # Get directory name as parameter set name
            name = os.path.basename(directory)
            
            # Create parameter set
            parameter_set = ParameterSet(name, directory)
            
            # Add to sidebar
            self.add_parameter_set(parameter_set)
    
    def _copy_parameter_set(self, parameter_set):
        """Copy a parameter set.
        
        Args:
            parameter_set: ParameterSet to copy
        """
        # Create new name
        new_name = f"{parameter_set.name}_copy"
        
        # Check if name already exists
        existing_names = [ps.name for ps in self.parameter_sets]
        if new_name in existing_names:
            # Add number if name already exists
            i = 1
            while f"{new_name}_{i}" in existing_names:
                i += 1
            new_name = f"{new_name}_{i}"
        
        # Show info dialog (in the real implementation, we would copy files)
        QMessageBox.information(
            self,
            "Copy Parameter Set",
            f"This would copy parameters from {parameter_set.name} to {new_name}"
        )
        
        # Create new parameter set with the same parameters
        new_parameter_set = ParameterSet(new_name, parameter_set.path.parent / new_name)
        
        # Add to sidebar
        self.add_parameter_set(new_parameter_set)
    
    def _delete_parameter_set(self, parameter_set):
        """Delete a parameter set.
        
        Args:
            parameter_set: ParameterSet to delete
        """
        # Confirm deletion
        result = QMessageBox.question(
            self,
            "Delete Parameter Set",
            f"Are you sure you want to delete {parameter_set.name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            # Remove from parameter sets
            self.parameter_sets.remove(parameter_set)
            
            # Remove from tree widget
            for i in range(self.tree_widget.topLevelItemCount()):
                item = self.tree_widget.topLevelItem(i)
                if item.data(0, Qt.UserRole) == parameter_set:
                    self.tree_widget.takeTopLevelItem(i)
                    break
            
            # If active, set another as active
            if parameter_set.is_active and self.parameter_sets:
                self.set_active_parameter_set(self.parameter_sets[0])
    
    def _edit_parameters(self, parameter_set, parameter_type):
        """Edit parameters.
        
        Args:
            parameter_set: ParameterSet containing the parameters
            parameter_type: Type of parameters to edit
        """
        # Create dialog based on parameter type
        dialog = None
        
        if parameter_type == "main":
            dialog = MainParameterDialog(parameter_set.main_params, self)
        
        if not dialog:
            QMessageBox.information(
                self,
                "Parameter Editor",
                f"Parameter editor for {parameter_type} not yet implemented in PyPTV2."
            )
            return
            
        # Show dialog
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            QMessageBox.information(
                self,
                "Parameters Updated",
                f"{parameter_type.capitalize()} parameters updated for {parameter_set.name}"
            )
    
    def _refresh_parameters(self):
        """Refresh parameters from disk."""
        # Placeholder implementation
        QMessageBox.information(
            self,
            "Refresh Parameters",
            "Parameter refresh not yet implemented in PyPTV2."
        )