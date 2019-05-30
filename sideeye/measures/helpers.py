"""
Helpers for calculating region measures.
"""

from typing import List, Any, Optional
from sideeye.data import Trial, Fixation, Region
from sideeye.types import RegionMeasure


def get_fp_fixations(trial: Trial, region_number: int) -> List[Fixation]:
    """Returns a list of fixations in the target region during first pass."""
    fp_fixations: List[Fixation] = []
    for fixation in trial.fixations:
        region = fixation.region
        if not region:
            break
        if region.number is not None and region.number > region_number:
            break
        if fp_fixations and region.number is not region_number:
            break
        if region.number is region_number and not fixation.excluded:
            fp_fixations += [fixation]

    return fp_fixations


def region_exists(trial: Trial, region_number: int) -> Region:
    """Raises an error if the target region does not exist."""
    if region_number >= len(trial.item.regions) or region_number < 0:
        raise ValueError("Region does not exist")
    return trial.item.get_region(region_number)


def save_measure(
    trial: Trial,
    region: Region,
    measure: str,
    value: Any,
    fixations: Optional[List[Fixation]],
) -> RegionMeasure:
    """Adds measure to region.measures, returns dictionary."""
    if region.number is not None:
        trial.region_measures[region.number][measure] = RegionMeasure(
            value=value, fixations=fixations
        )
    return RegionMeasure(value=value, fixations=fixations)


def save_trial_measure(trial: Trial, measure: str, value: Any) -> Any:
    """Adds measure to trial.measures, returns dictionary."""
    trial.trial_measures[measure] = value
    return value
