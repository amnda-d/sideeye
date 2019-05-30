"""
A Saccade is the period of time between two fixations. The start of the Saccade
is the Fixation before the Saccade, and the end is the Fixation after the Saccade.
If the location of the end Fixation is earlier in the Item the location of the
start Fixation, the Saccade is a regression.
"""

import json
from sideeye.data.fixation import Fixation


class Saccade:
    """
    Represents a saccade as the time in milliseconds between two fixations.

    Args:
        duration (int): Duration in milliseconds of the saccade.
        regression (bool): True if the saccade is a regression, false otherwise.
        start (Fixation): The fixation before the saccade.
        end (Fixation): The fixation after the saccade.
    """

    def __init__(self, duration: int, regression: bool, start: Fixation, end: Fixation):
        if duration < 0:
            raise ValueError("Duration of saccade must be positive.")

        self.duration: int = duration
        self.regression: bool = regression
        self.start: Fixation = start
        self.end: Fixation = end

    def __eq__(self, other) -> bool:
        """Check if two Saccades are equivalent"""
        return self.__dict__ == other.__dict__

    def __str__(self) -> str:
        """Convert Saccade into a string."""
        return json.dumps(
            {
                "duration": self.duration,
                "regression": self.regression,
                "start": self.start,
                "end": self.end,
            },
            default=lambda x: str(x) if isinstance(x, Fixation) else x.__dict__,
        )
