"""
A Region represents the boundaries of a region in an Item as (character, line)
points in the text of the Item. A region also has a label, number, and optionally
the text contained in the region.
"""

class Region:
    """
    Represents a Region as x and y coordinates for character positions of the
    beginning and end of the Region.

    Attributes:
        start (Point): The character and line position of the beginning of the Region.
        end (Point): The character and line position of the end of the Region.
        text (str, optional): Text contained in the region.
        label (str, optional): A label for the region.
        number (int, optional): A number identifier for the region.

    Args:
        start (Point): The character and line position of the beginning of the Region.
        end (Point): The character and line position of the end of the Region.
        text (str, optional): Text contained in the region.
        label (str, optional): A label for the region.
        number (int, optional): A number identifier for the region.
    """

    def __init__(self, start, end, text="", label='undefined', number=None):
        if start > end:
            raise ValueError('End of region must be after start of region.')
        if start.x < 0 or start.y < 0 or end.x < 0 or end.y < 0:
            raise ValueError('Region cannot have negative start and end.')

        self.start = start
        self.end = end
        self.label = label
        self.text = text
        self.number = number

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return ('(start: '
                + str(self.start)
                + ', end: '
                + str(self.end)
                + ', label: '
                + str(self.label)
                + ', number: '
                + str(self.number)
                + ', text: '
                + str(self.text)
                + ')')
