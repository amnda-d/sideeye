"""
This module contains functions for parsing experiments.

"""

import json
import os
from .. import parser

def load_config(config_file):
    """Load a JSON config file into a dictionary."""
    with open(config_file) as cfg:
        return json.load(cfg)

def parse(da1_file, region_file, config_file='sideeye/default_config.json'):
    """
    Given a DA1 file and region file, and config file, parse an Experiment. If
    config is not provided, default config will be used.

    Args:
        da1_file (str): Name of DA1 file.
        region_file: Name of region file (.cnt or .reg).
        config_file: Name of configuration file.
    """
    config = load_config(config_file)
    region_config = config['region_fields']
    da1_config = config['da1_fields']
    cutoffs = config['cutoffs']
    verbose = config['terminal_output']

    items = parser.region.file(region_file,
                               region_config['number'],
                               region_config['condition'],
                               region_config['boundaries_start'],
                               region_config['includes_y'],
                               verbose=verbose)

    experiment = parser.da1.parse(da1_file,
                                  items,
                                  da1_config['index'],
                                  da1_config['number'],
                                  da1_config['condition'],
                                  da1_config['time'],
                                  da1_config['fixation_start'],
                                  cutoffs['min'],
                                  cutoffs['max'],
                                  cutoffs['include_fixation'],
                                  cutoffs['include_saccades'],
                                  verbose=verbose)
    return experiment

def parse_dir(da1_directory, region_file, config_file='sideeye/default_config.json'):
    """
    Given a directory of DA1 files, a region file, and config file, parse all DA1 files in
    the directory into Experiments. If config is not provided, default config will be used.

    Args:
        da1_directory: Name of directory containing DA1 files.
        region_file: Name of region file (.cnt or .reg).
        config_file: Name of configuration file.
    """
    config = load_config(config_file)
    da1s = os.listdir(da1_directory)

    region_config = config['region_fields']
    da1_config = config['da1_fields']
    cutoffs = config['cutoffs']
    verbose = config['terminal_output']

    items = parser.region.file(region_file,
                               region_config['number'],
                               region_config['condition'],
                               region_config['boundaries_start'],
                               region_config['includes_y'],
                               verbose=verbose)
    experiments = []
    for da1 in da1s:
        if da1[-4:].lower() != '.da1':
            print('Skipping %s: not a DA1 file.' % da1)
        else:
            experiments += [parser.da1.parse(os.path.join(da1_directory, da1),
                                             items,
                                             da1_config['index'],
                                             da1_config['number'],
                                             da1_config['condition'],
                                             da1_config['time'],
                                             da1_config['fixation_start'],
                                             cutoffs['min'],
                                             cutoffs['max'],
                                             cutoffs['include_fixation'],
                                             cutoffs['include_saccades'],
                                             verbose=verbose)]

    return experiments
