"""
Region-based eye-tracking measures. These measures are calculated for each region
of each trial in an experiment.

Many of these measures use a list of first pass fixations in the region in calculating the measure. First pass fixations are defined as:

::

    def get_first_pass_fixations(trial, region_number):
        first_pass_fixations = []

        for fixation in trial:
            if fixation.region_number > region_number:
                break
            if length of first_pass_fixations > 0 and fixation.region_number is not region_number:
                break
            if fixation.region_number is region_number and fixation is not excluded:
                first_pass_fixations += [fixation]

        return first_pass_fixations
"""

from .boolean import (
    skip,
    first_pass_regressions_in,
    first_pass_regressions_out
    )

from .other import landing_position, launch_site, first_pass_fixation_count

from .duration import (
    first_fixation_duration,
    single_fixation_duration,
    first_pass,
    go_past,
    total_time,
    right_bounded_time,
    reread_time,
    second_pass,
    spillover_time,
    refixation_time,
    go_back_time_char,
    go_back_time_region
    )

__all__ = [
    'skip',
    'first_pass_regressions_in',
    'first_pass_regressions_out',
    'landing_position',
    'launch_site',
    'first_pass_fixation_count',
    'first_fixation_duration',
    'single_fixation_duration',
    'first_pass',
    'go_past',
    'total_time',
    'right_bounded_time',
    'reread_time',
    'second_pass',
    'spillover_time',
    'refixation_time',
    'go_back_time_char',
    'go_back_time_region'

]
