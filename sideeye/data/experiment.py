"""
An Experiment is the highest-level data object in the SideEye module, representing
a single participant's data.
"""

from datetime import datetime
from typing import List, Dict
from sideeye.data.trial import Trial
from sideeye.types import Condition, ItemNum, ItemId


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
        filename (Optional[str]): Optional name of source file.
        date (Optional[datetime]): Optional date.
    """

    def __init__(
        self, name: str, trials: List[Trial], filename: str = "", date: datetime = None
    ):
        self.name: str = name
        self.trials: Dict[ItemId, Trial] = {}
        self.filename: str = filename
        self.date: datetime = date if date else datetime.now()
        self.trial_indices: Dict[int, ItemId] = {}
        for trial in trials:
            self.trials[(trial.item.number, trial.item.condition)] = trial
            self.trial_indices[trial.index] = (trial.item.number, trial.item.condition)

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __str__(self) -> str:
        return "name: {}\nfilename: {}\ndate: {}\ntrials: [\n{}\n]".format(
            self.name,
            self.filename,
            self.date,
            ",\n".join([str(trial) for trial in self.trials]),
        )

    def get_trial(
        self, number: ItemNum = None, condition: Condition = None, index: int = None
    ) -> Trial:
        """
        Get a trial by item number and condition, or by index if specified.

        Args:
            number (ItemNum): Trial number.
            condition (Condition): Trial condition.
            index (int): Trial index.
        """
        if index:
            return self.trials[self.trial_indices[index]]
        if number and condition:
            return self.trials[(number, condition)]
        raise ValueError("Either index or condition and number must be provided.")
