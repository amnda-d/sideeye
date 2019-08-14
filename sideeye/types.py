"""
Mypy types aliases.
"""

from typing import Tuple, Union, DefaultDict, Dict, Any, List, Optional
from mypy_extensions import TypedDict
from sideeye.data.fixation import Fixation


class RegionMeasure(TypedDict):
    """Region measure dict."""

    value: Any
    fixations: Optional[List[Fixation]]


Condition = str
ItemNum = str
ItemId = Tuple[ItemNum, Condition]
Measures = DefaultDict[int, DefaultDict[str, Union[Dict, RegionMeasure]]]
TrialMeasures = DefaultDict[str, Dict]
