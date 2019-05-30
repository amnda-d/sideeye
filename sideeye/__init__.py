"""
SideEye is a Python package for processing eye tracking data that interfaces
with EyeTrack and Experiment Builder.
"""

from .data import *
from .calculate import calculate_measure, calculate_all_measures
from .output import (
    generate_region_output,
    generate_trial_output,
    generate_all_output_wide_format,
    generate_all_output,
)
from . import parser
from . import measures
