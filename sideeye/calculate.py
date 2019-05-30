"""
This module contains functions for calculating measures on parsed experiments.
Calculated measures are saved as a dictionary in the `measures` attribute of the
experiment. These functions do not return anything, they only calculate the measure
or measures on each trial or region of the experiments.
"""

from typing import List
from sideeye import measures
from sideeye.config import Configuration
from sideeye.output import generate_all_output, generate_all_output_wide_format
from sideeye.data import Experiment


def calculate_measure(experiments: List[Experiment], measure: str, verbose: int = 0):
    """
    Given an array of experiments and the name of a measure, calculate the measure for
    every trial in the experiment.

    Args:
        experiments (List[Experiment]): List of experiments to calculate measures for.
        measure (str): Name of measure to calculate.
        verbose (int): Debugging output level.
    """
    if hasattr(measures.trial, measure):
        for experiment in experiments:
            if verbose >= 3:
                print(
                    "Calculating measure: %s for experiment: %s"
                    % (measure, experiment.name)
                )
            for trial in experiment.trials.values():
                if verbose >= 4:
                    print("\t...for trial: %s" % trial.index)
                if not trial.trial_measures[measure]:
                    getattr(measures.trial, measure)(trial)

    elif hasattr(measures.region, measure):
        for experiment in experiments:
            if verbose >= 3:
                print(
                    "Calculating measure: %s for experiment: %s"
                    % (measure, experiment.name)
                )
            for trial in experiment.trials.values():
                if verbose >= 4:
                    print("\t...for trial: %s" % trial.index)
                for region in trial.item.regions:
                    if (
                        region.number is not None
                        and not trial.region_measures[region.number][measure]
                    ):
                        getattr(measures.region, measure)(trial, region.number)
    else:
        raise ValueError('Measure "%s" does not exist.' % measure)


def calculate_all_measures(
    experiments: List[Experiment],
    output_file: str = None,
    config: Configuration = Configuration(),
):
    """
    Given an array of experiments and config file, calculate all measures specified in the
    config file for the experiment, and optionally output the results as a csv.

    Args:
        experiments (List[Experiment]): List of experiments to calculate measures for.
        output_file (str): Name of output file. if `None`, no file is produced.
        config (Configuration): SideEye configuration.
    """
    wide_format = config.wide_format

    for measure in config.measures.names:
        calculate_measure(experiments, measure, config.terminal_output)

    output_text = (
        generate_all_output_wide_format(experiments, config)
        if wide_format
        else generate_all_output(experiments, config)
    )
    if output_file is not None:
        with open(output_file, "w") as output:
            output.write(output_text)

    return output_text
