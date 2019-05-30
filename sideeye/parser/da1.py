"""
A file parser for DA1 data files.
"""
import os
from typing import List, Dict
from sideeye.data import Point, Fixation, Trial, Experiment, Item
from sideeye.types import ItemNum, Condition
from sideeye.config import Configuration


def validate(filename: str, fixations_first_col: int, da1_type: str = None):
    """Checks if a file is in DA1 format."""
    if filename[-4:].lower() != ".da1":
        raise ValueError("%s Failed validation: Not a DA1 file" % filename)
    with open(filename) as da1_file:
        line = [int(x) for x in da1_file.readline().split()]
        if (len(line) - fixations_first_col) % 4 != 0:
            raise ValueError(
                "%s Failed validation: Does not match DA1 file format" % filename
            )
        if da1_type == "robodoc" and line[3] < line[-1]:
            raise ValueError("%s Failed validation: Not a robodoc DA1 file" % filename)


def parse(
    filename: str,
    items: Dict[ItemNum, Dict[Condition, Item]],
    config: Configuration = Configuration(),
    da1_type: str = None,
) -> Experiment:
    """
    Parses DA1-like files into sideeye Experiment objects, given column positions.

    Args:
        filename (str): DA1 file.
        items (Dict[ItemNum, Dict[Condition, Item]]): List of items in the experiment.
        da1_type (str): Type of DA1 file - `timdrop`, `robodoc`, or `None` for any other type.
    """
    if config.terminal_output > 0:
        print("\nParsing DA1 file: %s" % filename)

    validate(filename, config.da1_fields.fixation_start, da1_type)

    def parse_fixations(line, item):
        """Parses a list of (x, y, start time, end time) numbers into a list of Fixations."""
        fixations = []
        for pos in range(0, len(line), 4):
            x_pos = line[pos]
            y_pos = line[pos + 1]
            start = line[pos + 2]
            end = line[pos + 3]
            if (end - start) > config.cutoffs.min and (
                config.cutoffs.max < 0 or (end - start) < config.cutoffs.max
            ):
                fixations += [
                    Fixation(
                        Point(x_pos, y_pos),
                        start,
                        end,
                        len(fixations),
                        item.find_region(x_pos, y_pos),
                    )
                ]
            else:
                fixations += [
                    Fixation(
                        Point(x_pos, y_pos),
                        start,
                        end,
                        len(fixations),
                        item.find_region(x_pos, y_pos),
                        excluded=True,
                    )
                ]

        return fixations

    with open(filename) as da1_file:
        trials: List[Trial] = []
        for da1_line in da1_file:
            split_line = da1_line.split()
            number = split_line[config.da1_fields.number]
            condition = split_line[config.da1_fields.condition]
            line: List[int] = [int(x) for x in split_line]
            if config.terminal_output == 2 or config.terminal_output >= 5:
                print("\tParsing trial: %s" % line[config.da1_fields.index])
            if items[number][condition]:
                fixations = parse_fixations(
                    line[config.da1_fields.fixation_start :], items[number][condition]
                )
                trials += [
                    Trial(
                        line[config.da1_fields.index],
                        line[config.da1_fields.time],
                        items[number][condition],
                        fixations,
                        config.cutoffs.include_fixation,
                        config.cutoffs.include_saccades,
                    )
                ]
            else:
                print(
                    "Item number",
                    number,
                    ", condition",
                    condition,
                    "does not exist. It was not added to the Experiment object.",
                )

        return Experiment(
            "".join(os.path.split(filename)[1].split(".")[:-1]), trials, filename
        )
