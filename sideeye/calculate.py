"""
This module contains functions for calculating measures on parsed experiments.
Calculated measures are saved as a dictionary in the `measures` attribute of the
experiment. These functions do not return anything, they only calculate the measure
or measures on each trial or region of the experiments.
"""

import json
import os
from typing import List
from . import measures
from .output import generate_all_output, generate_all_output_wide_format
from .types import Config
from .data import Experiment

DEFAULT_CONFIG: str = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'default_config.json'
)

def load_config(config_file: str) -> Config:
    """Load a JSON config file into a dictionary."""
    with open(config_file) as cfg:
        return json.load(cfg)

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
                print('Calculating measure: %s for experiment: %s' % (measure, experiment.name))
            for trial in experiment.trials.values():
                if verbose >= 4:
                    print('\t...for trial: %s' % trial.index)
                if not trial.trial_measures[measure]:
                    getattr(measures.trial, measure)(trial)

    elif hasattr(measures.region, measure):
        for experiment in experiments:
            if verbose >= 3:
                print('Calculating measure: %s for experiment: %s' % (measure, experiment.name))
            for trial in experiment.trials.values():
                if verbose >= 4:
                    print('\t...for trial: %s' % trial.index)
                for region in trial.item.regions:
                    if region.number is not None and not trial.region_measures[region.number][measure]:
                        getattr(measures.region, measure)(trial, region.number)
    else:
        raise ValueError('Measure "%s" does not exist.' % measure)

def calculate_all_measures(
        experiments: List[Experiment],
        output_file: str = None,
        config_file: str = DEFAULT_CONFIG
    ):
    """
    Given an array of experiments and config file, calculate all measures specified in the
    config file for the experiment, and optionally output the results as a csv.

    Args:
        experiments (List[Experiment]): List of experiments to calculate measures for.
        output_file (str): Name of output file. if `None`, no file is produced.
        config_file (str): Configuration filename.
    """
    config = load_config(config_file)
    wide_format = config['wide_format']
    region_measures = config['region_measures']
    trial_measures = config['trial_measures']
    verbose = config['terminal_output']

    for measure in region_measures.keys():
        calculate_measure(experiments, measure, verbose)

    for measure in trial_measures.keys():
        calculate_measure(experiments, measure, verbose)

    output_text = (
        generate_all_output_wide_format(experiments, config_file)
        if wide_format
        else generate_all_output(experiments, config_file)
    )
    if output_file is not None:
        with open(output_file, 'w') as output:
            output.write(output_text)

    return output_text
