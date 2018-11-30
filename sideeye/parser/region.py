"""
A file parser for region data files.
"""
from collections import defaultdict

from ..data import Point, Region, Item

def text(string):
    """
    A parser for region strings, with regions separated by ``/``.

    Single-line Example: ``This is region 1/ This is region 2/ This is region 3/ This is region 4.``

    Multi-line Example: ``This is region 1/ This is region 2/ This is``\n
                        ``region 3/ This is region 4.``
    """
    if not isinstance(string, str):
        raise ValueError('Not a region string.')
    string = string.rstrip('\n').split('/')
    regions = []
    line = 0
    char = 0
    for region in string:
        start = Point(char, line)
        region = region.replace('\\n', '\n')
        if '\n' in region:
            line += 1
            char = 0
        char += len(region.split('\n')[-1])
        end = Point(char, line)
        regions += [Region(
            start,
            end,
            len([c for c in region if c != '\n']),
            region.strip('\n')
            )]
    return regions

def textfile(filename, verbose=0):
    """
    A parser for a region text file, with regions separated by ``/`` and lines
    within an item separated by ``\n``. ``\n`` is ignored in counting the length
    of a region.

    Each line should contain one Item, with the item number, followed by a space or
    tab (``\t``), the item condition, another space or tab, and the region string.

    For example: ``1    2   This is item one /condition two.\n/There are two
    lines /and four regions.
    """
    if verbose > 0:
        print('\nParsing region text file: %s' % filename)

    if filename[-4:].lower() != '.txt':
        raise ValueError('%s Failed validation: Not a region file' % filename)

    with open(filename, 'r') as region_file:
        items = defaultdict(lambda: defaultdict(bool))
        for line in region_file:
            line = line.split(maxsplit=2)
            number = int(line[0])
            condition = int(line[1])
            if verbose == 2 or verbose >= 5:
                print('\tParsing item: %s, condition: %s' % (number, condition))
            items[number][condition] = Item(number,
                                            condition,
                                            text(line[2]))
        return items

def validate_region_file(filename):
    """Checks if a file is a region file."""
    if filename[-4:].lower() != '.cnt' and filename[-4:].lower() != '.reg':
        raise ValueError('%s Failed validation: Not a region file' % filename)

def file(filename,
         number_location,
         condition_location,
         boundaries_start=3,
         includes_y=False,
         verbose=0):
    """
    Parses a .reg or .cnt file into a dictionary of sideeye Item objects.

    Args:
        filename (str): Region filename.
        number_location (int): Item number column location.
        condition_location (int): Condition number column location.
        boundaries_start (int): Column location of first region boundary start.
        includes_y (bool): Whether or not the region boundaries specify line position.
    """
    if verbose > 0:
        print('\nParsing region file: %s' % filename)

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

    with open(filename, 'r') as region_file:
        items = defaultdict(lambda: defaultdict(bool))
        for line in region_file:
            line = [int(x) for x in line.split()]
            condition = line[condition_location]
            number = line[number_location]
            if verbose == 2 or verbose >= 5:
                print('\tParsing item: %s, condition: %s' % (number, condition))
            items[number][condition] = Item(number,
                                            condition,
                                            line_to_regions(line[boundaries_start:]))
        return items
