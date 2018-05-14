"""
A Fixation represents a period of time where a participant fixated on an item
in a trial. Fixation position is represented by character and line position in
the item. A Fixation can also hold information about the region of the item it
occurred in, and whether or not it has been excluded by fixation cutoff
parameters. If the x or y position of the fixation is -1, the fixation is excluded.
"""

class Fixation:
    """
    Represents a single Fixation by location, start time, and end time.

    Attributes:
        char (int or None): Character position of the fixation. None of position
                            is negative.
        line (int or None): Line position of the fixation. None if position is
                            negative.
        duration (int): Total time of Fixation (end - start) in milliseconds.
        start (int): Start time of Fixation in milliseconds since trial start.
        end (int): End time of Fixation in milliseconds since trial start.
        region (Region): Region the Fixation occurred in.
        index (int): Index of where the Fixation occurred in a trial.
        excluded (bool): Whether or not the fixation will be excluded from calculations.

    Args:
        position (Point): The character and line position of the Fixation, zero-indexed.
        start (int): Start time for the Fixation, in milliseconds.
        end (int): End time for the Fixation, in milliseconds.
        region (Region, optional): Region the Fixation occurs in, can be initially unassigned.
        index (int, optional): An index of where the fixation occurred in a trial.
        excluded (boolean, optional): Whether the fixation should be excluded from calculations.
    """

    def __init__(self, position, start, end, region=None, index=None, excluded=False):
        if start > end or start < 0 or end < 0:
            raise ValueError('Invalid start or end time.')

        if position.x < 0 or position.y < 0:
            self.excluded = True
        else:
            self.excluded = excluded

        self.char = position.x
        self.line = position.y
        self.start = start
        self.end = end
        self.region = region
        self.duration = end - start
        self.index = index

    def __eq__(self, other):
        if self.region:
            return self.__dict__ == other.__dict__
        else:
            return (self.char == other.char
                    and self.line == other.line
                    and self.start == other.start
                    and self.end == other.end
                    and self.duration == other.duration
                    and self.excluded == other.excluded)

    def __str__(self):
        return ('(char: '
                + str(self.char)
                + ', line: '
                + str(self.line)
                + ', start: '
                + str(self.start)
                + 'ms, end: '
                + str(self.end)
                + 'ms, region: '
                + str(self.region)
                + ', excluded: '
                + str(self.excluded)
                + ')')

    def assign_region(self, region):
        """
        Assign a Region object to the Fixation.

        Args:
            region (Region): Region to assign to the fixation.
        """
        self.region = region
