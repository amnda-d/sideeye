"""
Helpers for calculating region measures.
"""

def get_fp_fixations(trial, region_number):
    """Returns a list of fixations in the target region during first pass."""
    fp_fixations = []
    for fixation in trial.fixations:
        if fixation.region.number > region_number:
            break
        if len(fp_fixations) is not 0 and fixation.region.number is not region_number:
            break
        if fixation.region.number is region_number and not fixation.excluded:
            fp_fixations += [fixation]

    return fp_fixations

def region_exists(trial, region_number):
    """Raises an error if the target region does not exist."""
    if region_number >= len(trial.item.regions) or region_number < 0:
        raise ValueError('Region does not exist')
    else:
        return trial.item.get_region(region_number)

def save_measure(trial, region, measure, value, fixations):
    """Adds measure to region.measures, returns dictionary."""
    trial.region_measures[region.number][measure] = {'value': value, 'fixations': fixations}
    return {'value': value, 'fixations': fixations}

def save_trial_measure(trial, measure, value):
    """Adds measure to trial.measures, returns dictionary."""
    trial.trial_measures[measure] = value
    return value
