"""
A Fixation represents a period of time where a participant fixated on an item
in a trial. Fixation position is represented by character and line position in
the item. A Fixation can also hold information about the region of the item it
occurred in, and whether or not it has been excluded by fixation cutoff
parameters. If the x or y position of the fixation is -1, the fixation is excluded.
"""

from sideeye.data.point import Point
from sideeye.data.region import Region


class Fixation:
    """
    Represents a single Fixation by location, start time, and end time.

    Attributes:
        char (Optional[int]): Character position of the fixation. None of position
                            is negative.
        line (Optional[int]): Line position of the fixation. None if position is
                            negative.
        start (int): Start time of Fixation in milliseconds since trial start.
        end (int): End time of Fixation in milliseconds since trial start.
        index (int): Index of where the Fixation occurred in a trial.
        region (Region): Region the Fixation occurred in.
        excluded (bool): Whether or not the fixation will be excluded from calculations.

    Args:
        position (Point): The character and line position of the Fixation, zero-indexed.
        start (int): Start time for the Fixation, in milliseconds.
        end (int): End time for the Fixation, in milliseconds.
        index (int): An index of where the fixation occurred in a trial.
        region (Region): Region the Fixation occurs in.
        excluded (Optional[boolean]): Whether the fixation should be excluded from calculations.
    """

    def __init__(
        self,
        position: Point,
        start: int,
        end: int,
        index: int,
        region: Region,
        excluded: bool = False,
    ):
        if start > end or start < 0 or end < 0:
            raise ValueError("Invalid start or end time.")

        self.excluded: bool = True if position.x < 0 or position.y < 0 else excluded
        self.char: int = position.x
        self.line: int = position.y
        self.start: int = start
        self.end: int = end
        self.region: Region = region
        self.index: int = index

    def __eq__(self, other) -> bool:
        if self.region:
            return self.__dict__ == other.__dict__
        return (
            self.char == other.char
            and self.line == other.line
            and self.start == other.start
            and self.end == other.end
            and self.excluded == other.excluded
        )

    def __str__(self) -> str:
        return "( char: {}, line: {}, start: {}, end: {}, region: {}, excluded: {} )".format(
            self.char, self.line, self.start, self.end, self.region, self.excluded
        )

    def duration(self) -> int:
        """Fixation duration in ms."""
        return self.end - self.start

    def assign_region(self, region: Region):
        """
        Assign a Region object to the Fixation.

        Args:
            region (Region): Region to assign to the fixation.
        """
        self.region = region
