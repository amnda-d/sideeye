"""
A Trial represents the data from a participant reading one item. An individual
Trial is identified by an index, and contains the total time spent reading the
Item, lists of Fixations and Saccades associated with the Trial, and a dictionary
of trial and region measures calculated for the Trial.
"""

from collections import defaultdict
from . import Saccade, Point

class Trial:
    """
    Represents an individual Trial in an experiment.

    Attributes:
        index (int): Trial index.
        time (int): Total time of trial in milliseconds.
        item (Item): Item corresponding to trial data.
        fixations (List[Fixation]): List of fixations in trial.
        saccades (List[Saccade]): A list of saccades in the trial.
        trial_measures (dict): Trial measures that have been calculated for the trial.
        region_measures (dict): Region measures that have been calculated for the trial.

    Args:
        index (int): An identifier for the Trial. Must be greater than or equal to 0.
        time (int): Total time of the Trial in milliseconds.
        item (Item): An Item corresponding to the Trial.
        fixations (List[Fixation]): A list of Fixations in the Trial.
        include_fixation (bool): Boolean indicating whether an excluded fixation should be
                                 included in a saccade.
        include_saccades (bool): Boolean indicating whether saccades surrounding an excluded
                                 fixation should be included in a saccade.
    """
    def __init__(self, index, time, item, fixations,
                 include_fixation=False, include_saccades=False):
        """Inits Trial class."""
        if index < 0:
            raise ValueError('Index must be greater than 0.')
        if item is None:
            raise ValueError('Trial must be associated with an Item.')
        if time is not None and time < 0:
            raise ValueError('Total time must be positive.')

        saccades = []
        saccade_start = None
        saccade_duration = 0
        for key, fixation in enumerate(fixations):
            if saccade_start is None:
                if fixation.excluded:
                    continue
                else:
                    saccade_start = fixation
            else:
                if not fixation.excluded:
                    if not fixations[key - 1].excluded or include_saccades:
                        saccade_duration += fixation.start - fixations[key - 1].end
                    if saccade_duration > 0:
                        if fixation.char is None or fixation.line is None:
                            saccades += [Saccade(saccade_duration,
                                                 True,
                                                 saccade_start,
                                                 fixation)]
                        elif saccade_start.char is None or saccade_start.line is None:
                            saccades += [Saccade(saccade_duration,
                                                 False,
                                                 saccade_start,
                                                 fixation)]
                        else:
                            saccades += [Saccade(saccade_duration,
                                                 Point(fixation.char, fixation.line) <
                                                 Point(saccade_start.char, saccade_start.line),
                                                 saccade_start,
                                                 fixation)]
                    saccade_start = fixation
                    saccade_duration = 0
                else:
                    if include_fixation:
                        saccade_duration += fixation.duration
                    if include_saccades:
                        saccade_duration += fixation.start - fixations[key - 1].end

        for (idx, fixation) in enumerate(fixations):
            fixation.index = idx

        self.index = index
        self.time = time
        self.item = item
        self.fixations = fixations
        self.saccades = saccades
        self.trial_measures = defaultdict(dict)
        self.region_measures = defaultdict(lambda: defaultdict(dict))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return ('(index: ' +
                str(self.index) +
                ', time: ' +
                str(self.time) +
                'ms, item: ' +
                str(self.item) +
                ', fixations: ' +
                str(len(self.fixations)) +
                ', saccades: ' +
                str(len(self.saccades)) +
                ')')

    def fixation_count(self):
        """Return the number of fixations in the item."""
        return len([fix for fix in self.fixations if not fix.excluded])
