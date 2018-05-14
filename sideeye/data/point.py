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

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x is other.x and self.y is other.y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __lt__(self, other):
        return self.y < other.y or (self.y is other.y and self.x < other.x)

    def __le__(self, other):
        return self.y < other.y or (self.y is other.y and self.x <= other.x)

    def __gt__(self, other):
        return self.y > other.y or (self.y is other.y and self.x > other.x)

    def __ge__(self, other):
        return self.y > other.y or (self.y is other.y and self.x >= other.x)
