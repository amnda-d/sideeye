"""
Mypy types aliases.
"""

from typing import Tuple, Union, DefaultDict, Dict, Any, List, Optional
from mypy_extensions import TypedDict
from .data import Fixation

class DA1Config(TypedDict):
    """DA1 parser configuration."""
    index: int
    condition: int
    number: int
    time: int
    fixation_start: int

class RegionConfig(TypedDict):
    """Region parser configuration."""
    number: int
    condition: int
    boundaries_start: int
    includes_y: bool

class CutoffsConfig(TypedDict):
    """Fixation cutoff configuration."""
    min: int
    max: int
    include_fixation: bool
    include_saccades: bool

class Config(TypedDict):
    """Configuration file dict."""
    wide_format: bool
    da1_fields: DA1Config
    region_fields: RegionConfig
    cutoffs: CutoffsConfig
    terminal_output: int
    region_measures: Dict[str, Dict]
    trial_measures: Dict[str, Dict]
    region_output: Dict[str, Dict]
    trial_output: Dict[str, Dict]

class RegionMeasure(TypedDict):
    """Region measure dict."""
    value: Any
    fixations: Optional[List[Fixation]]

Condition = Union[str, int]
ItemNum = Union[str, int]
ItemId = Tuple[ItemNum, Condition]
RegionMeasures = DefaultDict[int, DefaultDict[str, Union[Dict, RegionMeasure]]]
TrialMeasures = DefaultDict[str, Dict]
