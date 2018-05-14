"""
This module contains functions for calculating measures on parsed experiments.
Calculated measures are saved as a dictionary in the `measures` attribute of the
experiment. These functions do not return anything, they only calculate the measure
or measures on each trial or region of the experiments.
"""

import json
from . import measures
from .output import generate_all_output

def load_config(config_file):
    """Load a JSON config file into a dictionary."""
    with open(config_file) as cfg:
        return json.load(cfg)

def calculate_measure(experiments, measure, verbose=0):
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
                    if not trial.region_measures[region.number][measure]:
                        getattr(measures.region, measure)(trial, region.number)
    else:
        raise ValueError('Measure "%s" does not exist.' % measure)

def calculate_all_measures(experiments,
                           output_file=None,
                           config_file='sideeye/default_config.json'):
    """
    Given an array of experiments and config file, calculate all measures specified in the
    config file for the experiment, and optionally output the results as a csv.

    Args:
        experiments (List[Experiment]): List of experiments to calculate measures for.
        output_file (str): Name of output file. if `None`, no file is produced.
        config_file (str): Configuration filename.
    """
    config = load_config(config_file)
    region_measures = config['region_measures']
    trial_measures = config['trial_measures']
    verbose = config['terminal_output']

    for measure in region_measures.keys():
        calculate_measure(experiments, measure, verbose)

    for measure in trial_measures.keys():
        calculate_measure(experiments, measure, verbose)

    if output_file is not None:
        with open(output_file, 'w') as output:
            output.write(generate_all_output(experiments, config_file))
