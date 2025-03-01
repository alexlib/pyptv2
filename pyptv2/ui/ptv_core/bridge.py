"""Bridge to PTV Core functionality."""

import numpy as np
import os
import sys
import yaml
from pathlib import Path

try:
    # Add openptv directory to Python path so we can import optv directly
    openptv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'openptv')
    if os.path.exists(openptv_path) and openptv_path not in sys.path:
        sys.path.insert(0, openptv_path)
    
    # Import OpenPTV modules
    try:
        # First try the direct import
        import optv.calibration as calibration
        import optv.correspondences as correspondences
        import optv.image_processing as image_processing
        import optv.parameters as parameters
        import optv.orientation as orientation
        import optv.segmentation as segmentation
        import optv.tracker as tracker
        import optv.tracking_framebuf as tracking_framebuf
        
        HAVE_OPENPTV = True
        print("OpenPTV modules imported directly")
    except ImportError as e:
        # Fall back to package import
        print(f"Direct import failed: {e}, trying package import")
        from pyptv2.openptv.optv import calibration
        from pyptv2.openptv.optv import correspondences
        from pyptv2.openptv.optv import image_processing
        from pyptv2.openptv.optv import parameters
        from pyptv2.openptv.optv import orientation
        from pyptv2.openptv.optv import segmentation
        from pyptv2.openptv.optv import tracker
        from pyptv2.openptv.optv import tracking_framebuf
        
        HAVE_OPENPTV = True
        print("OpenPTV modules imported from package")
except ImportError as e:
    print(f"Warning: OpenPTV modules could not be imported: {e}")
    HAVE_OPENPTV = False


class PTVCoreBridge:
    """Bridge to the OpenPTV core functionality."""
    
    def __init__(self, exp_path=None, software_path=None):
        """Initialize the PTV core bridge.
        
        Args:
            exp_path (Path, optional): Path to experiment directory
            software_path (Path, optional): Path to software directory
        """
        self.exp_path = Path(exp_path) if exp_path else Path.cwd()
        self.software_path = Path(software_path) if software_path else Path.cwd()
        
        self.n_cams = 4  # Default number of cameras
        self.initialized = False
        
        # Parameters
        self.param_path = self.exp_path / "parameters"
        self.yaml_params = {}
        
        # Experiment data
        self.cameras = []
        self.cal_img_base = None
        self.ori_img_base = None
        self.target_file = None
        self.current_frame = None
        
        # Detected targets and matches
        self.targets = []
        self.matched_particles = []
        self.correspondence_flags = []
    
    def initialize(self):
        """Initialize the experiment configuration and load images.
        
        Returns:
            list: List of images, one per camera
        """
        print(f"Initializing experiment at {self.exp_path}")
        
        # Load parameters
        self._load_parameters()
        
        # In a real implementation, we would load camera calibration data
        # and initialize the OpenPTV modules
        if HAVE_OPENPTV:
            # This is a placeholder for future implementation
            # Setup calibration
            pass
            
        self.initialized = True
        
        # Create placeholder images (gray backgrounds)
        images = []
        for i in range(self.n_cams):
            img = np.ones((480, 640), dtype=np.uint8) * 200
            # Add camera number to image
            for y in range(230, 250):
                for x in range(280, 360):
                    img[y, x] = 100
            images.append(img)
        
        return images
    
    def _load_parameters(self):
        """Load parameters from YAML files."""
        # Check if parameters directory exists
        if not self.param_path.exists():
            print(f"Parameters directory not found: {self.param_path}")
            # Use default parameters
            self._use_default_parameters()
            return
        
        # Look for YAML parameters
        yaml_files = list(self.param_path.glob("*.yaml"))
        if not yaml_files:
            print("No YAML parameter files found, using defaults")
            self._use_default_parameters()
            return
        
        # Load unified configuration if available
        config_yaml = self.param_path / "ptv.yaml"
        if config_yaml.exists():
            try:
                with open(config_yaml, 'r') as f:
                    self.yaml_params = yaml.safe_load(f)
                print(f"Loaded unified configuration from {config_yaml}")
            except Exception as e:
                print(f"Error loading YAML configuration: {e}")
                self._use_default_parameters()
        else:
            # Load individual YAML files
            self._load_individual_yaml_files()
    
    def _load_individual_yaml_files(self):
        """Load parameters from individual YAML files."""
        yaml_files = list(self.param_path.glob("*.yaml"))
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    params = yaml.safe_load(f)
                    param_name = yaml_file.stem
                    self.yaml_params[param_name] = params
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
    
    def _use_default_parameters(self):
        """Use default parameters when no files are available."""
        # Basic default parameters
        self.yaml_params = {
            "General": {
                "num_cams": 4,
                "img_size_x": 640,
                "img_size_y": 480
            },
            "Sequence": {
                "first_frame": 10000,
                "last_frame": 10004
            },
            "Calibration": {
                "cal_img_base": "cal/cam",
                "ori_img_base": "cal/ori"
            },
            "Processing": {
                "highpass_size": 5,
                "threshold": 20
            },
            "Tracking": {
                "search_radius": 10.0,
                "min_corr": 0.5,
                "angle_limit": 30.0
            }
        }
    
    def apply_highpass(self):
        """Apply highpass filter to images.
        
        Returns:
            list: List of filtered images
        """
        if not self.initialized:
            print("Error: System not initialized")
            return []
        
        images = []
        
        if HAVE_OPENPTV:
            # Here we would use the OpenPTV image_processing module
            # For now, we simulate the output
            for i in range(self.n_cams):
                img = np.ones((480, 640), dtype=np.uint8) * 180
                # Add some simulated particles
                for j in range(20):
                    x, y = np.random.randint(20, 620), np.random.randint(20, 460)
                    img[y-2:y+3, x-2:x+3] = 255
                images.append(img)
        else:
            # Use placeholder implementation
            for i in range(self.n_cams):
                img = np.ones((480, 640), dtype=np.uint8) * 180
                # Add some simulated particles
                for j in range(20):
                    x, y = np.random.randint(20, 620), np.random.randint(20, 460)
                    img[y-2:y+3, x-2:x+3] = 255
                images.append(img)
        
        return images
    
    def detect_particles(self):
        """Detect particles in images.
        
        Returns:
            tuple: Lists of x and y coordinates for each camera
        """
        if not self.initialized:
            print("Error: System not initialized")
            return [], []
        
        x_coords = []
        y_coords = []
        
        if HAVE_OPENPTV:
            # In a real implementation, we would use the segmentation module
            # For now, we generate placeholder data
            for i in range(self.n_cams):
                # Generate random particle positions
                n_particles = np.random.randint(20, 50)
                x = np.random.randint(20, 620, size=n_particles).tolist()
                y = np.random.randint(20, 460, size=n_particles).tolist()
                
                x_coords.append(x)
                y_coords.append(y)
            
            # Store the detected targets
            self.targets = [(x, y) for x, y in zip(x_coords, y_coords)]
        else:
            # Use placeholder implementation
            for i in range(self.n_cams):
                # Generate random particle positions
                n_particles = np.random.randint(20, 50)
                x = np.random.randint(20, 620, size=n_particles).tolist()
                y = np.random.randint(20, 460, size=n_particles).tolist()
                
                x_coords.append(x)
                y_coords.append(y)
        
        return x_coords, y_coords
    
    def find_correspondences(self):
        """Find correspondences between camera views.
        
        Returns:
            list: List of correspondence results
        """
        if not self.initialized:
            print("Error: System not initialized")
            return []
        
        if HAVE_OPENPTV:
            # In a real implementation, we would use the correspondences module
            # For now, we generate placeholder data
            correspondence_results = [
                {
                    "x": [[100, 200, 300], [150, 250, 350], [120, 220, 320], [130, 230, 330]],
                    "y": [[100, 200, 300], [150, 250, 350], [120, 220, 320], [130, 230, 330]],
                    "color": "red"
                },
                {
                    "x": [[400, 500], [450, 550], [420, 520], [430, 530]],
                    "y": [[400, 500], [450, 550], [420, 520], [430, 530]],
                    "color": "green"
                },
                {
                    "x": [[600], [650], [620], [630]],
                    "y": [[600], [650], [620], [630]],
                    "color": "blue"
                }
            ]
        else:
            # Use placeholder implementation
            correspondence_results = [
                {
                    "x": [[100, 200, 300], [150, 250, 350], [120, 220, 320], [130, 230, 330]],
                    "y": [[100, 200, 300], [150, 250, 350], [120, 220, 320], [130, 230, 330]],
                    "color": "red"
                },
                {
                    "x": [[400, 500], [450, 550], [420, 520], [430, 530]],
                    "y": [[400, 500], [450, 550], [420, 520], [430, 530]],
                    "color": "green"
                },
                {
                    "x": [[600], [650], [620], [630]],
                    "y": [[600], [650], [620], [630]],
                    "color": "blue"
                }
            ]
        
        return correspondence_results
    
    def track_particles(self):
        """Track particles through a sequence.
        
        Returns:
            bool: Success flag
        """
        if not self.initialized:
            print("Error: System not initialized")
            return False
        
        if HAVE_OPENPTV:
            # In a real implementation, we would use the tracker module
            # For now, we just return success
            return True
        else:
            # Use placeholder implementation
            return True
    
    def get_trajectories(self):
        """Get trajectory data.
        
        Returns:
            list: Trajectory data for each camera
        """
        if not self.initialized:
            print("Error: System not initialized")
            return []
        
        trajectory_data = []
        
        if HAVE_OPENPTV:
            # In a real implementation, we would load trajectory data from files
            # For now, we generate placeholder data
            for i in range(self.n_cams):
                # Generate simulated trajectory data
                n_trajectories = 10
                
                # Heads (start points)
                heads_x = np.random.randint(50, 600, size=n_trajectories).tolist()
                heads_y = np.random.randint(50, 400, size=n_trajectories).tolist()
                
                # Tails (middle points)
                tails_x = []
                tails_y = []
                for j in range(n_trajectories):
                    # Create a few points per trajectory
                    n_points = np.random.randint(3, 8)
                    tx = [heads_x[j] + np.random.randint(-30, 30) for _ in range(n_points)]
                    ty = [heads_y[j] + np.random.randint(-30, 30) for _ in range(n_points)]
                    tails_x.extend(tx)
                    tails_y.extend(ty)
                
                # Ends (final points)
                ends_x = [x + np.random.randint(-30, 30) for x in heads_x]
                ends_y = [y + np.random.randint(-30, 30) for y in heads_y]
                
                trajectory_data.append({
                    "heads": {
                        "x": heads_x,
                        "y": heads_y,
                        "color": "blue"
                    },
                    "tails": {
                        "x": tails_x,
                        "y": tails_y,
                        "color": "green"
                    },
                    "ends": {
                        "x": ends_x,
                        "y": ends_y,
                        "color": "red"
                    }
                })
        else:
            # Use placeholder implementation
            for i in range(self.n_cams):
                # Generate simulated trajectory data
                n_trajectories = 10
                
                # Heads (start points)
                heads_x = np.random.randint(50, 600, size=n_trajectories).tolist()
                heads_y = np.random.randint(50, 400, size=n_trajectories).tolist()
                
                # Tails (middle points)
                tails_x = []
                tails_y = []
                for j in range(n_trajectories):
                    # Create a few points per trajectory
                    n_points = np.random.randint(3, 8)
                    tx = [heads_x[j] + np.random.randint(-30, 30) for _ in range(n_points)]
                    ty = [heads_y[j] + np.random.randint(-30, 30) for _ in range(n_points)]
                    tails_x.extend(tx)
                    tails_y.extend(ty)
                
                # Ends (final points)
                ends_x = [x + np.random.randint(-30, 30) for x in heads_x]
                ends_y = [y + np.random.randint(-30, 30) for y in heads_y]
                
                trajectory_data.append({
                    "heads": {
                        "x": heads_x,
                        "y": heads_y,
                        "color": "blue"
                    },
                    "tails": {
                        "x": tails_x,
                        "y": tails_y,
                        "color": "green"
                    },
                    "ends": {
                        "x": ends_x,
                        "y": ends_y,
                        "color": "red"
                    }
                })
        
        return trajectory_data