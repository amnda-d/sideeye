"""
This module contains functions for parsing experiments.

"""

from typing import List
from sideeye.parser import region, da1, asc
from sideeye.data import Experiment
from sideeye.config import Configuration


def parse(
    experiment_file: str, region_file: str, config: Configuration = Configuration()
) -> Experiment:
    """
    Given a DA1 file and region file, and config file, parse an Experiment. If
    config is not provided, default config will be used.

    Args:
        experiment_file (str): Name of DA1 or ASC file.
        region_file: Name of region file (.cnt, .reg, or .txt).
        config (Configuration): Configuration.
    """
    verbose = config.terminal_output

    if region_file[-4:].lower() == ".txt":
        items = region.textfile(region_file, verbose=verbose)
    else:
        items = region.file(region_file, config, verbose=verbose)

    if experiment_file[-4:].lower() == ".da1":
        experiment = da1.parse(experiment_file, items, config)
    if experiment_file[-4:].lower() == ".asc":
        experiment = asc.parse(experiment_file, items, config.asc_parsing)
    return experiment


def parse_files(
    experiment_files: List[str],
    region_file: str,
    config: Configuration = Configuration(),
) -> List[Experiment]:
    """
    Given a list of DA1 or ASC files, a region file, and config file, parse all files in
    the list into Experiments. If config is not provided, default config will be used.

    Args:
        experiment_files: List of DA1 or ASC files.
        region_file: Name of region file (.cnt, .reg, or .txt).
        config (Config): Configuration.
    """
    verbose = config.terminal_output

    if region_file[-4:].lower() == ".txt":
        items = region.textfile(region_file, verbose=verbose)
    else:
        items = region.file(region_file, config, verbose=verbose)
    experiments: List[Experiment] = []
    for experiment_file in experiment_files:
        if experiment_file[-4:].lower() == ".da1":
            experiments += [da1.parse(experiment_file, items, config)]
        elif experiment_file[-4:].lower() == ".asc":
            experiments += [asc.parse(experiment_file, items, config.asc_parsing)]
        else:
            print("Skipping %s: not a DA1 or ASC file." % experiment_file)

    return experiments
