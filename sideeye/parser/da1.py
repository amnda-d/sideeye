"""
A file parser for DA1 data files.
"""
import os
from typing import List, Dict
from ..data import Point, Fixation, Trial, Experiment, Item
from ..types import ItemNum, Condition

def parse_timdrop(
        filename: str,
        items: Dict[ItemNum, Dict[Condition, Item]],
        min_cutoff: int = -1,
        max_cutoff: int = -1,
        include_fixation: bool = False,
        include_saccades: bool = False,
        verbose: int = 0
    ) -> Experiment:
    """
    Parses timdrop-formatted DA1 files into sideeye Experiment objects.

    Args:
        filename (str): DA1 file.
        items (Dict[ItemNum, Dict[Condition, Item]]): List of items in the experiment.
        min_cutoff (int): Cutoff for minimum fixation duration. Use -1 for no cutoff.
        max_cutoff (int): Cutoff for maximum fixation duration. Use -1 for no cutoff.
        include_fixation (bool): Whether excluded fixations should be included in saccades.
                                 See :ref:`Trials <Trial>` for more information.
        include_saccades (bool): Whether saccades surrounding an excluded fixation
                                 should be included in a saccade. See :ref:`Trials <Trial>`
                                 for more information.
    """
    return parse(
        filename=filename,
        items=items,
        index_col=0,
        number_col=2,
        condition_col=1,
        time_col=-1,
        fixations_first_col=8,
        min_cutoff=min_cutoff,
        max_cutoff=max_cutoff,
        include_fixation=include_fixation,
        include_saccades=include_saccades,
        da1_type='timdrop',
        verbose=verbose
    )

def parse_robodoc(
        filename: str,
        items: Dict[ItemNum, Dict[Condition, Item]],
        min_cutoff: int = -1,
        max_cutoff: int = -1,
        include_fixation: bool = False,
        include_saccades: bool = False,
        verbose: int = 0
    ) -> Experiment:
    """
    Parses robodoc-formatted DA1 files into sideeye Experiment objects.

    Args:
        filename (str): DA1 file.
        items (Dict[ItemNum, Dict[Condition, Item]]): List of items in the experiment.
        min_cutoff (int): Cutoff for minimum fixation duration. Use -1 for no cutoff.
        max_cutoff (int): Cutoff for maximum fixation duration. Use -1 for no cutoff.
        include_fixation (bool): Whether excluded fixations should be included in saccades.
                                 See :ref:`Trials <Trial>` for more information.
        include_saccades (bool): Whether saccades surrounding an excluded fixation
                                 should be included in a saccade. See :ref:`Trials <Trial>`
                                 for more information.
    """
    return parse(
        filename=filename,
        items=items,
        index_col=0,
        number_col=2,
        condition_col=1,
        time_col=3,
        fixations_first_col=8,
        min_cutoff=min_cutoff,
        max_cutoff=max_cutoff,
        include_fixation=include_fixation,
        include_saccades=include_saccades,
        da1_type='robodoc',
        verbose=verbose
    )

def validate(filename: str, fixations_first_col: int, da1_type: str = None):
    """Checks if a file is in DA1 format."""
    if filename[-4:].lower() != '.da1':
        raise ValueError('%s Failed validation: Not a DA1 file' % filename)
    with open(filename) as da1_file:
        line = [int(x) for x in da1_file.readline().split()]
        if (len(line) - fixations_first_col) % 4 != 0:
            raise ValueError('%s Failed validation: Does not match DA1 file format' % filename)
        if da1_type == 'robodoc' and line[3] < line[-1]:
            raise ValueError('%s Failed validation: Not a robodoc DA1 file' % filename)

def parse(
        filename: str,
        items: Dict[ItemNum, Dict[Condition, Item]],
        index_col: int,
        number_col: int,
        condition_col: int,
        time_col: int,
        fixations_first_col: int,
        min_cutoff: int,
        max_cutoff: int,
        include_fixation: bool,
        include_saccades: bool,
        da1_type: str = None,
        verbose: int = 0
    ) -> Experiment:
    """
    Parses DA1-like files into sideeye Experiment objects, given column positions.

    Args:
        filename (str): DA1 file.
        items (Dict[ItemNum, Dict[Condition, Item]]): List of items in the experiment.
        index_col (int): Trial index column position.
        number_col (int): Item number column position.
        condition_col (int): Item condition column position.
        time_col (int): Total trial time column position.
        fixations_first_col (int): Column position where first fixation of trial begins.
        min_cutoff (int): Cutoff for minimum fixation duration. Use -1 for no cutoff.
        max_cutoff (int): Cutoff for maximum fixation duration. Use -1 for no cutoff.
        include_fixation (bool): Whether excluded fixations should be included in saccades.
                                 See :ref:`Trials <Trial>` for more information.
        include_saccades (bool): Whether saccades surrounding an excluded fixation
                                 should be included in a saccade. See :ref:`Trials <Trial>`
                                 for more information.
        da1_type (str): Type of DA1 file - `timdrop`, `robodoc`, or `None` for any other type.
    """
    if verbose > 0:
        print('\nParsing DA1 file: %s' % filename)

    validate(filename, fixations_first_col, da1_type)

    def parse_fixations(line, item):
        """Parses a list of (x, y, start time, end time) numbers into a list of Fixations."""
        fixations = []
        for pos in range(0, len(line), 4):
            x_pos = line[pos]
            y_pos = line[pos + 1]
            start = line[pos + 2]
            end = line[pos + 3]
            if (end - start) > min_cutoff and (max_cutoff < 0 or (end - start) < max_cutoff):
                fixations += [Fixation(
                    Point(x_pos, y_pos),
                    start,
                    end,
                    len(fixations),
                    item.find_region(x_pos, y_pos)
                )]
            else:
                fixations += [
                    Fixation(
                        Point(x_pos, y_pos),
                        start,
                        end,
                        len(fixations),
                        item.find_region(x_pos, y_pos),
                        excluded=True
                    )
                ]

        return fixations

    with open(filename) as da1_file:
        trials: List[Trial] = []
        for da1_line in da1_file:
            line: List[int] = [int(x) for x in da1_line.split()]
            number = line[number_col]
            condition = line[condition_col]
            if verbose == 2 or verbose >= 5:
                print('\tParsing trial: %s' % line[index_col])
            if items[number][condition]:
                fixations = parse_fixations(line[fixations_first_col:], items[number][condition])
                trials += [
                    Trial(
                        line[index_col],
                        line[time_col],
                        items[number][condition],
                        fixations,
                        include_fixation,
                        include_saccades
                    )
                ]
            else:
                print(
                    'Item number',
                    number,
                    ', condition',
                    condition,
                    'does not exist. It was not added to the Experiment object.'
                )

        return Experiment(''.join(os.path.split(filename)[1].split('.')[:-1]), trials, filename)
