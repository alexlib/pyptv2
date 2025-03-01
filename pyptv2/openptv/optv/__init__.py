"""Python binding for the OpenPTV library (liboptv).

This package provides Python bindings to the C implementation of the OpenPTV
algorithms for 3D particle tracking velocimetry.
"""

from . import calibration
from . import correspondences
from . import epipolar
from . import image_processing
from . import imgcoord
from . import orientation
from . import parameters
from . import segmentation
from . import tracker
from . import tracking_framebuf
from . import transforms
from . import vec_utils

__all__ = [
    'calibration',
    'correspondences',
    'epipolar',
    'image_processing',
    'imgcoord',
    'orientation',
    'parameters',
    'segmentation',
    'tracker',
    'tracking_framebuf',
    'transforms',
    'vec_utils'
]
