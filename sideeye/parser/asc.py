"""
A parser for .ASC files.
"""

import re
import os
from datetime import datetime
from math import sqrt
from typing import Optional, Dict, List, Tuple
from mypy_extensions import TypedDict
from sideeye.data import Fixation, Point, Trial, Item, Experiment
from sideeye.config import Configuration, ASCParsingConfig
from sideeye.types import Condition, ItemNum


class CharPosition(TypedDict, total=False):
    """Position of character in pixels."""

    char: str
    x1: int
    x2: int
    y1: int
    y2: int
    char_pos: int
    line_pos: int


LINE_TYPES = ["MSG", "EFIX", "EBLINK", "SYNCTIME"]
ITEM_REGEX = re.compile(r"E(?P<condition>.+)I(?P<item>.+)D(?P<dependent>.+)")
CHAR_REGEX = re.compile(
    r"CHAR.+(?P<char>.)\s+(?P<x1>.+)\s+(?P<y1>.+)\s+(?P<x2>.+)\s+(?P<y2>.+)"
)
FIX_REGEX = re.compile(
    r"EFIX\s+\w+\s+(?P<start>\d+)\s+(?P<end>\d+)\s+(?P<dur>.+)\s+(?P<x>[\d.]+)\s+(?P<y>[\d.]+)\s+.+"
)
END_REGEX = re.compile(r".+\s+(?P<end>.+)\s+TRIAL_RESULT")
BLINK_REGEX = re.compile(r"EBLINK\s+.+\s+.+\s+(?P<blink_dur>.+)")
START_REGEX = re.compile(r".+\s+(?P<start>.+)\s+SYNCTIME")


def get_condition(line: str) -> Optional[str]:
    """Returns item condition in line."""
    match = ITEM_REGEX.search(line)
    return match.group("condition") if "TRIALID" in line and match else None


def get_item(line: str) -> Optional[str]:
    """Returns item number in line."""
    match = ITEM_REGEX.search(line)
    return match.group("item") if "TRIALID" in line and match else None


def get_char(line: str) -> Optional[CharPosition]:
    """Returns displayed character and location."""
    char = CHAR_REGEX.search(line)
    return (
        CharPosition(
            char=char.group("char"),
            x1=int(char.group("x1")),
            x2=int(char.group("x2")),
            y1=int(char.group("y1")),
            y2=int(char.group("y2")),
        )
        if char
        else None
    )


def get_start(line: str) -> Optional[int]:
    """Returns start time of trial."""
    match = START_REGEX.search(line)
    return int(match.group("start")) if match else None


def get_end(line: str) -> Optional[int]:
    """Returns end time of trial."""
    match = END_REGEX.search(line)
    return int(match.group("end")) if match else None


def get_blink_dur(line: str) -> Optional[int]:
    """Returns duration of blink."""
    match = BLINK_REGEX.search(line)
    return int(match.group("blink_dur")) if match else None


def dist(x_1: float, x_2: float, y_1: float, y_2: float) -> float:
    """Returns distance between point (x_1, y_1) and (x_2, y_2)."""
    return sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def get_lines(characters: List[CharPosition]) -> List[CharPosition]:
    """Converts list of character locations into a list containing a list
    of characters for each line of text."""
    characters = sorted(characters, key=lambda x: x["y1"])
    lines: List[List[CharPosition]] = []
    max_y1 = 0
    max_y2 = 0
    for char in characters:
        if char["y1"] > max_y2:
            lines += [[]]
        if char["y1"] > max_y1:
            max_y1 = char["y1"]
        if char["y2"] > max_y2:
            max_y2 = char["y2"]
        lines[-1] += [char]
    character_lines: List[List[CharPosition]] = [
        [
            CharPosition(
                char=char["char"],
                x1=char["x1"],
                x2=char["x2"],
                y1=char["y1"],
                y2=char["y2"],
                line_pos=line_pos,
                char_pos=char_pos,
            )
            for (char_pos, char) in enumerate(sorted(line, key=lambda x: x["x1"]))
        ]
        for (line_pos, line) in enumerate(lines)
    ]
    return [char for line in character_lines for char in line]


def get_fixation(
    line: str, characters: List[CharPosition], item: Item, index: int, time_offset: int
) -> Tuple[Optional[Fixation], int]:
    """Returns a Fixation object."""
    fix = FIX_REGEX.search(line)
    if fix:
        fix_x = float(fix.group("x"))
        fix_y = float(fix.group("y"))
        characters = get_lines(characters)

        for char in characters:
            if (char["x1"] < fix_x < char["x2"]) and (char["y1"] < fix_y < char["y2"]):
                offset = time_offset if time_offset else int(fix.group("start"))
                return (
                    Fixation(
                        Point(char["char_pos"], char["line_pos"]),
                        int(fix.group("start")) - offset,
                        int(fix.group("end")) - offset,
                        index,
                        item.find_region(char["char_pos"], char["line_pos"]),
                    ),
                    offset,
                )
    return None, time_offset


def get_new_fixations(
    new_fixation: Fixation,
    fixations: List[Fixation],
    config: ASCParsingConfig = Configuration().asc_parsing,
) -> List[Fixation]:
    """Append a new fixation or merge with the previous fixation."""
    if fixations and new_fixation.duration() < config.fixation_min_cutoff:
        old_fix = fixations[-1]
        return fixations[:-1] + [
            Fixation(
                Point(old_fix.char, old_fix.line),
                old_fix.start,
                new_fixation.end,
                old_fix.index,
                old_fix.region,
            )
        ]
    if fixations and fixations[-1].duration() < config.fixation_min_cutoff:
        old_fix = fixations[-1]
        return fixations[:-1] + [
            Fixation(
                Point(new_fixation.char, new_fixation.line),
                old_fix.start,
                new_fixation.end,
                old_fix.index,
                new_fixation.region,
            )
        ]
    return fixations[:] + [new_fixation]


def get_trials(
    asc: str,
    items: Dict[Condition, Dict[ItemNum, Item]],
    config: ASCParsingConfig = Configuration().asc_parsing,
) -> List[Trial]:
    """
    Parses .ASC text into a list of Trial objects.

    Args:
        asc (string): Text of .ASC file.
        items (Dict[str, Dict[str, Item]]): List of items in experiments.
        config (ASCParsingConfig): Configuration for .ASC parsing.
    """
    characters: List[CharPosition] = []
    fixations: List[Fixation] = []
    fixation_start_time = 0
    trials: List[Trial] = []
    exclude = False
    blinks = 0
    start_time = 0
    condition: Optional[str] = None
    item: Optional[str] = None
    for line in asc.split("\n"):
        if line.split() and line.split()[0] in LINE_TYPES:
            start_time = get_start(line) or start_time
            condition = get_condition(line) or condition
            item = get_item(line) or item
            char = get_char(line)
            characters = characters + [char] if char else characters
            new_fixation, fixation_start_time = (
                get_fixation(
                    line,
                    characters,
                    items[item][condition],
                    len(fixations),
                    fixation_start_time,
                )
                if start_time
                and item
                and condition
                and item in items
                and condition in items[item]
                else (None, fixation_start_time)
            )
            fixations = (
                get_new_fixations(new_fixation, fixations, config)
                if new_fixation
                else fixations
            )
            if (
                config.max_saccade_dur
                and len(fixations) > 1
                and fixations[-1].start - fixations[-2].end > config.max_saccade_dur
            ):
                exclude = True
            blink_dur = get_blink_dur(line)
            if blink_dur:
                blinks += 1
                if config.blink_max_dur and blink_dur > config.blink_max_dur:
                    exclude = True
                if config.blink_max_count and blinks > config.blink_max_count:
                    exclude = True
            end_time = get_end(line)
            if end_time:
                if (
                    item
                    and condition
                    and item in items
                    and condition in items[item]
                    and not exclude
                ):
                    trials += [
                        Trial(
                            len(trials),
                            end_time - start_time,
                            items[item][condition],
                            fixations,
                        )
                    ]
                start_time = 0
                fixations = []
                fixation_start_time = 0
                characters = []
                exclude = False
                blinks = 0
                item = None
                condition = None
    return trials


def parse(
    asc_file: str,
    items: Dict[Condition, Dict[ItemNum, Item]],
    config: ASCParsingConfig = Configuration().asc_parsing,
):
    """
    Parses a .ASC file into an Experiment object.

    Args:
        asc_file (string): Path to .ASC file.
        items (Dict[str, Dict[str, Item]]): List of items in experiments.
        config (ASCParsingConfig): Configuration for .ASC parsing.
    """
    with open(asc_file) as file:
        trials = get_trials(file.read(), items, config)
        return Experiment(
            "".join(os.path.split(asc_file)[1].split(".")[:-1]),
            trials,
            asc_file,
            datetime.fromtimestamp(os.path.getmtime(asc_file)),
        )
