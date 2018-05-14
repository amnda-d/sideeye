"""
Region-based eye-tracking measures. These measures are calculated for each region
of each trial in an experiment.
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
    refixation_time
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
    'refixation_time'
]
