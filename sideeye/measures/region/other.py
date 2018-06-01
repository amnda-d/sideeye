"""
Region-based eye tracking measures with fixation count or position output.
"""

from ..helpers import get_fp_fixations, region_exists, save_measure

def landing_position(trial, region_number):
    """
    The location relative to the beginning of the region (in
    number of characters) of the first fixation during the first pass, where the
    first character in the region is at position (0, 0). If the region was skipped,
    this measure is None.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if (length of fp_fixations is not 0
                and fp_fixations[0].char is not None
                and fp_fixations[0].line is not None):
            return (fp_fixations[0].char - region.start.char,
                    fp_fixations[0].line - region.start.line)

        else:
            return None

    """
    region = region_exists(trial, region_number)
    landing_pos = None
    fixation = None
    fp_fixations = get_fp_fixations(trial, region_number)

    if (len(fp_fixations) != 0 and fp_fixations[0].char is not None
            and fp_fixations[0].line is not None):
        landing_pos = '"(%s, %s)"' % (fp_fixations[0].char - region.start.x,
                                      fp_fixations[0].line - region.start.y)
        fixation = fp_fixations[0]

    return save_measure(trial, region, 'landing_position', landing_pos, fixation)

def launch_site(trial, region_number):
    """
    The location of the last fixation prior to the first fixation
    in the region. This measure returns an (x, y) tuple, where x is either the
    number of characters from the the beginning of the target region and y is the
    number of lines from the beginning of the region. -1 indicates the last character
    of the region preceding the target region, or the preceding line, and increasing
    negative numbers indicate further launch sites. If the region was skipped this
    measure is None.

    ::

        fixations = [fixation for fixation in trial if fixation is not excluded]

        for (index, fixation) in enumerate(fixations):
            if fixation.region_number > region_number:
                break
            if fixation.region_number == region_number:
                if index == 0:
                    break

                if fixations[index - 1].char is None:
                    launch_char = fixations[index - 1].char
                else:
                    launch_char = fixations[index - 1].char - fixation.region.start.char

                if fixations[index - 1].line is None:
                    launch_line = fixations[index - 1].line
                else:
                    launch_line = fixations[index - 1].line - fixation.region.start.line

                return (launch_char, launch_line)

        return None

    """
    region = region_exists(trial, region_number)
    launch = None
    fixation = None
    trial_fixations = [fix for fix in trial.fixations if not fix.excluded]

    for (idx, fixation) in enumerate(trial_fixations):
        if fixation.region.number > region_number:
            break
        if fixation.region.number == region_number:
            if idx == 0:
                break
            if trial_fixations[idx - 1].char is None:
                launch_char = trial_fixations[idx - 1].char
            else:
                launch_char = trial_fixations[idx - 1].char - fixation.region.start.x
            if trial_fixations[idx - 1].line is None:
                launch_line = trial_fixations[idx - 1].line
            else:
                launch_line = trial_fixations[idx - 1].line - fixation.region.start.y
            launch = '"(%s, %s)"' % (launch_char, launch_line)
            fixation = trial_fixations[idx - 1]
            break

    return save_measure(trial, region, 'launch_site', launch, fixation)

def first_pass_fixation_count(trial, region_number):
    """
    The number of fixations made in a region before leaving it during first pass.
    If the region was skipped this measure is None.

    ::

        fp_fixations = get_first_pass_fixations(trial, region_number)

        if length of fp_fixations is 0:
            return None
        else:
            return length of fp_fixations

    """
    region = region_exists(trial, region_number)
    fp_fixations = get_fp_fixations(trial, region_number)

    if len(fp_fixations) is 0:
        return save_measure(trial, region, 'first_pass_fixation_count', None, None)

    else:
        return save_measure(trial,
                            region,
                            'first_pass_fixation_count',
                            len(fp_fixations),
                            fp_fixations)
