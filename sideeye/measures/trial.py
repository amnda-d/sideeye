"""
Trial-based eye-tracking measures. These measures are calculated for each trial of an experiment.
"""

from .helpers import save_trial_measure

def location_first_regression(trial):
    """
    (x, y) character position of the last fixation before the first regression saccade
    in the trial, where a regression is defined as a saccade where the position of
    the fixation at the beginning of the saccade is later in the item than the
    position of the fixation at the end of the saccade. None if there are no regressions.

    ::

        for saccade in trial:
            if saccade is regression:
                return (saccade.start_fixation.char, saccade.start_fixation.line)
            else:
                return None
    """
    for saccade in trial.saccades:
        if saccade.regression:
            return save_trial_measure(trial,
                                      'location_first_regression',
                                      '"(%s, %s)"' % (saccade.start.char, saccade.start.line))
    return save_trial_measure(trial, 'location_first_regression', None)

def latency_first_regression(trial):
    """
    Time until the end of the fixation before the first regression saccade in the trial,
    where a regression is defined as a saccade where the position of the fixation at
    the beginning of the saccade is later in the item than the position of the fixation
    at the end of the saccade. None if there are no regressions.

    ::

        for saccade in trial:
            if saccade is regression:
                return saccade.start_fixation.end_time
            else:
                return None

    """
    for saccade in trial.saccades:
        if saccade.regression:
            return save_trial_measure(trial, 'latency_first_regression', saccade.start.end)
    return save_trial_measure(trial, 'latency_first_regression', None)

def fixation_count(trial):
    """
    Total number of non-excluded fixations in a trial.

    ::

        return length of [non-excluded fixations in trial]

    """
    return save_trial_measure(trial,
                              'fixation_count',
                              len([fix for fix in trial.fixations if not fix.excluded]))

def percent_regressions(trial):
    """
    Proportion of saccades that are regressions from the location of the previous fixation,
    where a regression is defined as a saccade where the position of the fixation at the
    beginning of the saccade is later in the item than the position of the fixation at
    the end of the saccade. None if there are no saccades.

    ::

        regressions = 0

        for saccade in trial:
            if saccade is regression:
                regressions += 1

        return regressions / (length of [trial.saccades])

    """
    regressions = 0

    for saccade in trial.saccades:
        if saccade.regression:
            regressions += 1.0

    if len(trial.saccades) == 0:
        return save_trial_measure(trial, 'percent_regressions', None)
    else:
        return save_trial_measure(trial, 'percent_regressions', regressions/len(trial.saccades))

def trial_total_time(trial):
    """
    Total time in the trial.

    ::

        return total trial time from .DA1 file OR end time of last non-excluded fixation

    """
    if trial.time is None:
        return save_trial_measure(trial,
                                  'trial_total_time',
                                  [fix for fix in trial.fixations if not fix.excluded][-1].end)
    return save_trial_measure(trial, 'trial_total_time', trial.time)

def average_forward_saccade(trial):
    """
    Average saccade duration between fixations moving forward through the sentence.

    ::

        forward_saccades = 0
        total_time = 0

        for saccade in trial:
            if saccade is not regression:
                forward_saccades += 1
                total_time += saccade.duration

        if forward_saccades is 0:
            return 0
        else:
            return total_time / forward_saccades

    """
    forward_saccades = 0.0
    total = 0.0

    for saccade in trial.saccades:
        if not saccade.regression:
            forward_saccades += 1.0
            total += saccade.duration

    if forward_saccades is 0.0:
        return save_trial_measure(trial, 'average_forward_saccade', 0)
    return save_trial_measure(trial, 'average_forward_saccade', total/forward_saccades)

def average_backward_saccade(trial):
    """
    Average saccade duration between fixations moving backward through the sentence, or the
    average duration of a regression saccade.

    ::

        backward_saccades = 0
        total_time = 0

        for saccade in trial:
            if saccade is regression:
                backward_saccades += 1
                total_time += saccade.duration

        if backward_saccades is 0:
            return 0
        else:
            return total_time / backward_saccades

    """
    backward_saccades = 0.0
    total = 0.0

    for saccade in trial.saccades:
        if saccade.regression:
            backward_saccades += 1.0
            total += saccade.duration

    if backward_saccades is 0.0:
        return save_trial_measure(trial, 'average_backward_saccade', 0)
    return save_trial_measure(trial, 'average_backward_saccade', total/backward_saccades)
