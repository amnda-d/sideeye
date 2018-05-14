"""
An Experiment is the highest-level data object in the SideEye module, representing
a single participant's data.
"""

from datetime import datetime

class Experiment:
    """
    Represents the data of one participant in an experiment.

    Attributes:
        name (str): Name of experiment.
        trials (dict): Dictionary mapping (number, condition) tuples to trials.
        filename (str): Name of file.
        date (Date): Date of experiment.
        trial_indices (dict): A dictionary mapping trial indices to (number, condition)
                              tuples. Used to locate trials.

    Args:
        name (str): A string name/identifier for the participant.
        trials (List[Trial]): Trials in the experiment.
        filename (str, optional): Optional name of source file.
        date (Date, optional): Optional date.
    """
    def __init__(self, name, trials, filename='', date=None):
        self.name = name
        self.trials = {}
        self.filename = filename
        self.date = date
        if date is None:
            self.date = datetime.now()
        else:
            self.date = date
        self.trial_indices = {}
        for trial in trials:
            self.trials[(trial.item.number, trial.item.condition)] = trial
            self.trial_indices[trial.index] = (trial.item.number, trial.item.condition)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return ('name: ' + str(self.name)
                + '\nfilename: ' + str(self.filename)
                + '\ndate: ' + str(self.date)
                + '\ntrials: ' + ', '.join([str(trial) for trial in self.trials]))

    def get_trial(self, number=None, condition=None, index=None):
        """
        Get a trial by item number and condition, or by index if specified.

        Args:
            number (int): Trial number.
            condition (int): Trial condition.
            index (int): Trial index.
        """
        if index != None:
            return self.trials[self.trial_indices[index]]
        if number != None and condition != None:
            return self.trials[(number, condition)]
        raise ValueError('Either index or condition and number must be provided.')
