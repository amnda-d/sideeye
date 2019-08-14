"""
A file parser for region data files.
"""
from collections import defaultdict
from typing import List, Dict, DefaultDict
from sideeye.data import Point, Region, Item
from sideeye.types import ItemNum, Condition
from sideeye.config import Configuration


def text(region_string: str) -> List[Region]:
    """
    A parser for region strings, with regions separated by ``/``.

    Single-line Example: ``This is region 1/ This is region 2/ This is region 3/ This is region 4.``

    Multi-line Example: ``This is region 1/ This is region 2/ This is``\n
                        ``region 3/ This is region 4.``
    """
    if not isinstance(region_string, str):
        raise ValueError("Not a region string.")
    string = region_string.rstrip("\n").split("/")
    regions: List[Region] = []
    line = 0
    char = 0
    for region in string:
        start = Point(char, line)
        region = region.replace("\\n", "\n")
        if "\n" in region:
            line += 1
            char = 0
        char += len(region.split("\n")[-1])
        end = Point(char, line)
        regions += [
            Region(
                start, end, len([c for c in region if c != "\n"]), region.strip("\n")
            )
        ]
    return regions


def textfile(filename: str, verbose: int = 0) -> Dict[ItemNum, Dict[Condition, Item]]:
    """
    A parser for a region text file, with regions separated by ``/`` and lines
    within an item separated by ``\\n``. ``\\n`` is ignored in counting the length
    of a region.

    Each line should contain one Item, with the item number, followed by a space or
    tab (``\\t``), the item condition, another space or tab, and the region string.

    For example: ``1    2   This is item one /condition two.\\n/There are two
    lines /and four regions.``
    """
    if verbose > 0:
        print("\nParsing region text file: %s" % filename)

    if filename[-4:].lower() != ".txt":
        raise ValueError("%s Failed validation: Not a region file" % filename)

    with open(filename, "r") as region_file:
        items: DefaultDict[ItemNum, Dict[Condition, Item]] = defaultdict(dict)
        for region_line in region_file:
            if region_line:
                line = region_line.split(maxsplit=2)
                number = line[0]
                condition = line[1]
                if verbose == 2 or verbose >= 5:
                    print("\tParsing item: %s, condition: %s" % (number, condition))
                items[number][condition] = Item(number, condition, text(line[2]))
        return items


def validate_region_file(filename: str):
    """Checks if a file is a region file."""
    if filename[-4:].lower() != ".cnt" and filename[-4:].lower() != ".reg":
        raise ValueError("%s Failed validation: Not a region file" % filename)


def file(
    filename: str, config: Configuration = Configuration(), verbose: int = 0
) -> Dict[ItemNum, Dict[Condition, Item]]:
    """
    Parses a .reg or .cnt file into a dictionary of sideeye Item objects.

    Args:
        filename (str): Region filename.
        config (Configuration): Configuration.
    """
    if verbose > 0:
        print("\nParsing region file: %s" % filename)

    number_location = config.region_fields.number
    condition_location = config.region_fields.condition
    boundaries_start = config.region_fields.boundaries_start
    includes_y = config.region_fields.includes_y

    validate_region_file(filename)

    def line_to_regions(line):
        """Helper function to convert a list of region boundaries into an item."""
        regions = []
        if includes_y:
            for boundary in range(0, len(line) - 3, 2):
                x_start = line[boundary]
                y_start = line[boundary + 1]
                x_end = line[boundary + 2]
                y_end = line[boundary + 3]
                regions += [Region(Point(x_start, y_start), Point(x_end, y_end))]
        else:
            for boundary in range(0, len(line) - 1):
                x_start = line[boundary]
                x_end = line[boundary + 1]
                regions += [Region(Point(x_start, 0), Point(x_end, 0))]
        return regions

    with open(filename, "r") as region_file:
        items: DefaultDict[ItemNum, Dict[Condition, Item]] = defaultdict(dict)
        for region_line in region_file:
            split_line = region_line.split()
            condition = split_line[condition_location]
            number = split_line[number_location]
            line = [int(x) for x in split_line]
            if verbose == 2 or verbose >= 5:
                print("\tParsing item: %s, condition: %s" % (number, condition))
            items[number][condition] = Item(
                number, condition, line_to_regions(line[boundaries_start:])
            )
        return items
