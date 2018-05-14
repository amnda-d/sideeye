"""
The data module contains SideEye's core data structures -  Experiments, Trials,
Items, Regions, Saccades, Fixations, and Points. Raw data can be parsed into
these objects, and measures can be calculated from them.
"""

from .point import Point
from .fixation import Fixation
from .saccade import Saccade
from .region import Region
from .item import Item
from .trial import Trial
from .experiment import Experiment

__all__ = ['Point', 'Fixation', 'Saccade', 'Region', 'Item', 'Trial', 'Experiment']
