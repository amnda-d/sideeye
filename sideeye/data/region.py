"""
A Region represents the boundaries of a region in an Item as (character, line)
points in the text of the Item. A region also has a label, number, and optionally
the text contained in the region.
"""

from typing import Union, Optional
from sideeye.data.point import Point


class Region:
    """
    Represents a Region as x and y coordinates for character positions of the
    beginning and end of the Region.

    Attributes:
        start (Point): The character and line position of the beginning of the Region.
        end (Point): The character and line position of the end of the Region.
        length (Optional[int]): Length of region in characters.
        text (Optional[str]): Text contained in the region.
        label (Optional[Union[str, int]]): A label for the region.
        number (Optional[int]): A number identifier for the region.

    Args:
        start (Point): The character and line position of the beginning of the Region.
        end (Point): The character and line position of the end of the Region.
        length (Optional[int]): Length of region in characters.
        text (Optional[str]): Text contained in the region.
        label (Optional[Union[str, int]]): A label for the region.
        number (Optional[int]): A number identifier for the region.
    """

    def __init__(
        self,
        start: Point,
        end: Point,
        length: int = None,
        text: str = "",
        label: Union[str, int] = "undefined",
        number: int = None,
    ):
        if start > end:
            raise ValueError("End of region must be after start of region.")
        if start.x < 0 or start.y < 0 or end.x < 0 or end.y < 0:
            raise ValueError("Region cannot have negative start and end.")
        if length and length < 0:
            raise ValueError("Region must have positive length.")

        self.start: Point = start
        self.end: Point = end
        self.length: Optional[int] = length
        self.label: Union[str, int] = label
        self.text: str = text
        self.number: Optional[int] = number

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __str__(self) -> str:
        return "(start: {}, end: {}, length: {}, label: {}, number: {}, text: {})".format(
            self.start, self.end, self.length, self.label, self.number, self.text
        )
