"""
A Point represents an (x, y) location. It is used to represent fixation positions
and region boundaries.
"""


class Point:
    """
    An (x, y) location.

    Attributes:
        x (int): x location.
        y (int): y location.
    """

    def __init__(self, x: int, y: int):
        self.x = x  # pylint: disable=invalid-name
        self.y = y  # pylint: disable=invalid-name

    def __eq__(self, other) -> bool:
        return self.x is other.x and self.y is other.y

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)

    def __lt__(self, other) -> bool:
        return self.y < other.y or (self.y is other.y and self.x < other.x)

    def __le__(self, other) -> bool:
        return self.y < other.y or (self.y is other.y and self.x <= other.x)

    def __gt__(self, other) -> bool:
        return self.y > other.y or (self.y is other.y and self.x > other.x)

    def __ge__(self, other) -> bool:
        return self.y > other.y or (self.y is other.y and self.x >= other.x)
