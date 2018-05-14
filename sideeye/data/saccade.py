"""
A Saccade is the period of time between two fixations. The start of the Saccade
is the Fixation before the Saccade, and the end is the Fixation after the Saccade.
If the location of the end Fixation is earlier in the Item the location of the
start Fixation, the Saccade is a regression.
"""

class Saccade:
    """
    Represents a saccade as the time in milliseconds between two fixations.

    Args:
        duration (int): Duration in milliseconds of the saccade.
        regression (bool): True if the saccade is a regression, false otherwise.
        start (Fixation): The fixation before the saccade.
        end (Fixation): The fixation after the saccade.
    """

    def __init__(self, duration, regression, start, end):
        if duration < 0:
            raise ValueError('Duration of saccade must be positive.')

        self.duration = duration
        self.regression = regression
        self.start = start
        self.end = end

    def __eq__(self, other):
        """Check if two Saccades are equivalent"""
        return self.__dict__ == other.__dict__

    def __str__(self):
        """Convert Saccade into a string."""
        return ('(duration: '
                + str(self.duration)
                + ', regression: '
                + str(self.regression)
                + ', start: '
                + str(self.start)
                + ', end: '
                + str(self.end)
                + ')')
