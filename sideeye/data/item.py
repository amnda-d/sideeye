"""
An Item represents the text that is displayed to a participant during a trial.
A number and condition identify the item, which consists of a list of regions,
and optionally a list of labels for the regions.
"""

from typing import Sequence, List, Union
from sideeye.types import ItemNum, Condition
from sideeye.data.region import Region


class Item:
    """
    Represents an Item in an experiment.

    Attributes:
        number (int): An identifier for the Item.
        condition (int): An identifier for the condition of the Item.
        regions (List[Region]): A list of Regions in the Item.
        labels (List[Union[int, str]]): A list of labels for the regions. If
                                         labels are not provided, integer indices
                                         are used. All labels are unique.
    Args:
        number (ItemNum): An identifier for the Item.
        condition (Condition): An identifier for the condition of the Item.
        regions (List[Region]): A list of Region objects in the Item. All regions
                                must be unique.
        labels (List[Union[int, str]]): A list of labels for regions. If not provided,
                                         integer indices will be used. All labels must be unique.
    """

    def __init__(
        self,
        number: ItemNum,
        condition: Condition,
        regions: List[Region],
        labels: Sequence[Union[int, str]] = None,
    ):
        """Inits Item class."""
        if labels and len(labels) != len(regions):
            raise ValueError("Number of regions must be equal to number of labels.")
        if labels and len(set(labels)) != len(labels):
            raise ValueError("Region labels must be unique")
        if not regions:
            raise ValueError("An Item must have at least one Region")
        for region in regions:
            if regions.count(region) > 1:
                raise ValueError("Regions must be unique.")

        self.labels: Sequence[Union[int, str]] = labels if labels else range(
            len(regions)
        )
        for key, region in enumerate(regions):
            region.label = self.labels[key]
            region.number = key

        self.number: ItemNum = number
        self.condition: Condition = condition
        self.regions: List[Region] = regions

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __str__(self) -> str:
        return "(number: {}, condition: {}, regions: [{}])".format(
            self.number, self.condition, ", ".join([str(r) for r in self.regions])
        )

    def get_region(self, label: Union[str, int]) -> Region:
        """
        Get Region with matching label.

        Args:
            label (Union[str, int]): A region label.
        """
        return self.regions[self.labels.index(label)]

    def find_region(self, x_pos: int, y_pos: int) -> Region:
        """
        Get the region containing position (x_pos, y_pos).

        Args:
            x_pos (int): X (character) position of a location.
            y_pos (int): Y (line) position of a location.
        """
        for region in range(1, len(self.regions)):
            current_x = self.regions[region].start.x
            current_y = self.regions[region].start.y
            if (current_x > x_pos and current_y >= y_pos) or (current_y > y_pos):
                return self.regions[region - 1]

        if (
            x_pos <= self.regions[-1].end.x and y_pos <= self.regions[-1].end.y
        ) or y_pos <= self.regions[-1].end.y:
            return self.regions[-1]

        raise ValueError(
            "Position: ("
            + str(x_pos)
            + ", "
            + str(y_pos)
            + ") is out of range for item: "
            + str(self)
        )

    def region_count(self) -> int:
        """Get the number of Regions in the Item."""
        return len(self.regions)
