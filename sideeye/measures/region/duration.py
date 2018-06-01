"""
Region-based eye tracking measures with duration(ms) output.
"""

from ..helpers import get_fp_fixations, region_exists, save_measure

def first_fixation_duration(trial, region_number):
    """
    The duration of the first fixation in a region during first pass reading
    (i.e., before the reader fixates areas beyond the region).
    If this region is skipped during first pass, this measure is None.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if length of fp_fixations is 0:
            return None
        else:
            return duration of first fixation in fp_fixations

    """
    region = region_exists(trial, region_number)
    fp_fixations = get_fp_fixations(trial, region_number)

    if len(fp_fixations) is 0:
        return save_measure(trial, region, 'first_fixation_duration', None, None)
    return save_measure(trial, region,
                        'first_fixation_duration',
                        fp_fixations[0].duration,
                        [fp_fixations[0]])

def single_fixation_duration(trial, region_number):
    """
    If there is only one fixation on the region during first pass reading, this
    measure is the duration of that fixation. If the region is skipped during
    first pass, the measure is None.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if length of fp_fixations is 1:
            return duration of fixation in fp_fixations
        else:
            return None

    """
    region = region_exists(trial, region_number)
    fp_fixations = get_fp_fixations(trial, region_number)

    if len(fp_fixations) is 1:
        return save_measure(trial, region,
                            'single_fixation_duration',
                            fp_fixations[0].duration,
                            [fp_fixations[0]])
    return save_measure(trial, region, 'single_fixation_duration', None, None)

def first_pass(trial, region_number):
    """
    The summed duration of all fixations in a region
    during first pass (i.e., before the reader fixates areas beyond the region).
    If this region is skipped during first pass, this measure is None.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if length of fp_fixations is 0:
            return None

        total = 0

        for fixation in fp_fixations:
            total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)
    fp_fixations = get_fp_fixations(trial, region_number)

    if len(fp_fixations) is 0:
        return save_measure(trial, region, 'first_pass', None, None)

    total = 0
    for fixation in fp_fixations:
        total += fixation.duration

    return save_measure(trial, region, 'first_pass', total, fp_fixations)

def go_past(trial, region_number):
    """
    Also known as regression path duration. The summed duration of all fixations
    starting from the first fixation in the region, including any fixations in
    prior regions until the reader goes past the region (i.e., before the reader
    fixates areas beyond the region). If this region is skipped during first pass,
    this measure is None.

    ::

        if length of get_first_pass_fixations(trial, region_number) is 0:
            return None

        total = 0

        for fixation in trial:
            if fixation is not excluded:
                if fixation.region_number > region_number:
                    break
                if total is not 0 or fixation.region_number is region_number:
                    total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)

    if len(get_fp_fixations(trial, region_number)) is 0:
        return save_measure(trial, region, 'go_past', None, None)

    gp_fixations = []
    total = 0
    for fixation in trial.fixations:
        if not fixation.excluded:
            if fixation.region.number > region_number:
                break
            if total is not 0 or fixation.region.number is region_number:
                gp_fixations += [fixation]
                total += fixation.duration

    return save_measure(trial, region, 'go_past', total, gp_fixations)

def total_time(trial, region_number):
    """
    The summed duration of all fixations in the region that
    occur at any time during the trial. If this region is never fixated this
    measure is 0.

    ::

        total = 0

        for fixation in trial:
            if fixation.region_number is region_number and fixation is not excluded:
                total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)

    region_fixations = []
    total = 0
    for fixation in trial.fixations:
        if fixation.region.number is region_number and not fixation.excluded:
            region_fixations += [fixation]
            total += fixation.duration

    return save_measure(trial, region, 'total_time', total, region_fixations)

def right_bounded_time(trial, region_number):
    """
    The summed duration of all fixations starting
    from the first fixation in the region, excluding any fixations in prior
    regions until the reader goes past the region (i.e., until the reader
    fixates areas beyond the region). If this region is skipped during first
    pass, this measure is None.

    ::

        if length of get_first_pass_fixations(trial, region_number) is 0:
            return None

        total = 0

        for fixation in trial:
            if fixation is not excluded:
                if fixation.region_number > region_number:
                    break
                if fixation.region_number is region_number:
                    total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)

    if len(get_fp_fixations(trial, region_number)) is 0:
        return save_measure(trial, region, 'right_bounded_time', None, None)

    rb_fixations = []
    total = 0
    for fixation in trial.fixations:
        if not fixation.excluded:
            if fixation.region.number > region_number:
                break
            if fixation.region.number is region_number:
                rb_fixations += [fixation]
                total += fixation.duration

    return save_measure(trial, region, 'right_bounded_time', total, rb_fixations)

def reread_time(trial, region_number):
    """
    The summed duration of all fixations in the region that occur after a region
    to the right has been fixated. If this region is never fixated this measure is 0.

    ::

        total = 0
        reread = False

        for fixation in trial:
            if fixation is not excluded:
                if fixation.region_number > region_number:
                    reread = True
                if reread and fixation.region_number is region_number:
                    total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)

    rr_fixations = []
    total = 0
    reread = False
    for fixation in trial.fixations:
        if not fixation.excluded:
            if fixation.region.number > region_number:
                reread = True
            if reread and fixation.region.number is region_number:
                rr_fixations += [fixation]
                total += fixation.duration

    return save_measure(trial, region, 'reread_time', total, rr_fixations)

def second_pass(trial, region_number):
    """
    The summed duration of all fixations in the region that occur on a region
    after that region has been exited in either direction for the first time.
    If this region is never fixated this measure is 0.

    ::

        total = 0
        first_pass = False
        exited = False

        for fixation in trial:
            if fixation is not excluded:
                if fixation.region_number is region_number:
                    first_pass = True
                if first_pass and fixation.region_number is not region_number:
                    exited = True
                if first_pass and exited and fixation.region_number is region_number:
                    total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)

    sp_fixations = []
    total = 0
    f_pass = False
    exited = False
    for fixation in trial.fixations:
        if not fixation.excluded:
            if fixation.region.number is region_number:
                f_pass = True
            if f_pass and fixation.region.number is not region_number:
                exited = True
            if f_pass and exited and fixation.region.number is region_number:
                sp_fixations += [fixation]
                total += fixation.duration

    return save_measure(trial, region, 'second_pass', total, sp_fixations)

def spillover_time(trial, region_number):
    """
    The duration of fixations on the region immediately following
    the region of interest, where the previous fixation was on the region of interest.
    If there are no such fixations, the measure is None.

    ::

        total = 0
        visited_region = False

        for fixation in trial:
            if fixation is not excluded:
                if visited_region and fixation.region_number is not region_number + 1:
                    visited_region = False
                if fixation.region_number is region_number:
                    visited_region = True
                if visited_region and fixation.region_number is region_number + 1:
                    total += fixation.duration

        if total is 0:
            return None

        return total

    """
    region = region_exists(trial, region_number)

    so_fixations = []
    total = 0
    visited_region = False
    for fixation in trial.fixations:
        if not fixation.excluded:
            if visited_region and fixation.region.number is not region_number + 1:
                visited_region = False
            if fixation.region.number is region_number:
                visited_region = True
            if visited_region and fixation.region.number is region_number + 1:
                so_fixations += [fixation]
                total += fixation.duration

    if total is 0:
        return save_measure(trial, region, 'spillover_time', None, None)
    return save_measure(trial, region, 'spillover_time', total, so_fixations)

def refixation_time(trial, region_number):
    """
    The sum of all first-pass fixations excluding the first
    fixation. If there was a single fixation in the region or it was skipped
    this measure is None.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if length of fp_fixations is 0 or 1:
            return None

        total = 0

        for fixation in fp_fixations[1:]:
            total += fixation.duration

        return total

    """
    region = region_exists(trial, region_number)
    fp_fixations = get_fp_fixations(trial, region_number)

    if len(fp_fixations) is 0 or len(fp_fixations) is 1:
        return save_measure(trial, region, 'refixation_time', None, None)

    total = 0
    for fixation in fp_fixations[1:]:
        total += fixation.duration

    return save_measure(trial, region, 'refixation_time', total, fp_fixations[1:])
