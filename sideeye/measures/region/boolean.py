"""
Region-based eye tracking measures with boolean output.
"""

from sideeye.measures.helpers import get_fp_fixations, region_exists, save_measure
from sideeye.data import Trial
from sideeye.types import RegionMeasure


def skip(trial: Trial, region_number: int) -> RegionMeasure:
    """
    True if the reader fixates a region beyond the target region before
    fixating the target region or the target region is never fixated, False otherwise.

    ::

        if length of get_first_pass_fixations(trial, region_number) is 0:
            return True
        else return False

    """
    region = region_exists(trial, region_number)
    return save_measure(
        trial, region, "skip", bool(not get_fp_fixations(trial, region_number)), None
    )


def first_pass_regressions_out(trial: Trial, region_number: int) -> RegionMeasure:
    """
    This measure is True if the reader made a regression out of the region on the
    first pass - that is, exited a region to the left after the first pass. The measure
    is False if they exited to the right, and None if the region was not fixated
    during first pass reading.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if length of fp_fixations is 0:
            return None

        next_fixation = next non-excluded fixation after last fixation in fp_fixations

        if next_fixation.region_number < region_number:
            return True
        else:
            return False

    """
    region = region_exists(trial, region_number)
    fp_fixations = get_fp_fixations(trial, region_number)

    if not fp_fixations:
        return save_measure(trial, region, "first_pass_regressions_out", None, None)

    try:
        next_fix_idx = fp_fixations[-1].index + 1
        next_fix = trial.fixations[next_fix_idx]
        while next_fix.excluded and next_fix_idx < len(trial.fixations):
            next_fix_idx += 1
            next_fix = trial.fixations[next_fix_idx]
        if (
            next_fix.region.number is not None
            and next_fix.region.number < region_number
        ):
            return save_measure(trial, region, "first_pass_regressions_out", True, None)
    except IndexError:
        return save_measure(trial, region, "first_pass_regressions_out", False, None)

    return save_measure(trial, region, "first_pass_regressions_out", False, None)


def first_pass_regressions_in(trial: Trial, region_number: int) -> RegionMeasure:
    """
    This measure is True if the reader made a fixation in the region
    after fixating on any region to the right of it, False if they only fixated
    on the region after fixating on regions to the left, and None if the region
    was never fixated.

    ::

        region_fixations = [all non-excluded fixations in region]

        if length of region_fixations is 0:
            return None

        for fixation in region_fixations:
            if previous_fixation.region_number > region_number:
                return True

        return False

    """
    region = region_exists(trial, region_number)
    trial_fixations = [fix for fix in trial.fixations if not fix.excluded]
    region_fixations = [
        key
        for key, fixation in enumerate(trial_fixations)
        if fixation.region.number is region_number
    ]

    if not region_fixations:
        return save_measure(trial, region, "first_pass_regressions_in", None, None)
    for fixation in region_fixations:
        prev_fix_region = trial_fixations[fixation - 1].region
        if (
            fixation
            and prev_fix_region.number is not None
            and prev_fix_region.number > region_number
        ):
            return save_measure(trial, region, "first_pass_regressions_in", True, None)
    return save_measure(trial, region, "first_pass_regressions_in", False, None)
