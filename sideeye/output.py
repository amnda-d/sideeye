"""
This module contains functions to generate csv reports of measures calculated
for experiments.
"""

import json
import os
from typing import Any, List, Dict, Optional
from .types import Config
from .data import Experiment, Trial, Region

DEFAULT_CONFIG: str = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'default_config.json'
)

def load_config(config_file: str) -> Config:
    """Loads a JSON config file into a dictionary."""
    with open(config_file) as cfg:
        return json.load(cfg)

def write_column(
        column: str,
        experiment: Experiment,
        trial: Trial,
        region: Optional[Region],
        measure: str,
        cutoff: int
    ) -> str:
    """Maps a column name to an output value."""
    output: Any = 'NA'
    if column == 'experiment_name':
        output = experiment.name
    elif column == 'filename':
        output = experiment.filename
    elif column == 'date':
        output = experiment.date
    elif column == 'trial_id':
        output = trial.index
    elif column == 'trial_total_time':
        output = trial.time
    elif column == 'item_id':
        output = trial.item.number
    elif column == 'item_condition':
        output = trial.item.condition
    elif column == 'region_label':
        if region is not None:
            output = region.label
    elif column == 'region_number':
        if region is not None:
            output = region.number
    elif column == 'region_text':
        if region is not None:
            output = region.text
    elif column == 'region_start':
        if region is not None:
            output = region.start
    elif column == 'region_end':
        if region is not None:
            output = region.end
    elif column == 'measure':
        output = measure
    elif column == 'value':
        if region is not None and region.number is not None:
            output = trial.region_measures[region.number][measure]['value']
        else:
            output = trial.trial_measures[measure]
        if cutoff >= 0 and isinstance(output, int) and output > cutoff:
            output = 'CUTOFF'
    return str(output)

def measure_output(
        measure: str,
        cutoff: int,
        columns: Dict[str, Dict],
        experiment: Experiment,
        trial: Trial,
        region: Optional[Region]
    ) -> str:
    """
    Generates a formatted output string for an individual measure.

    Args:
        measure (str): Name of measure.
        cutoff (int): Cutoff value for measure. Use -1 for no cutoff.
        columns (Dict[str, Dict]): Dict of columns to output.
        experiment (Experiment): Experiment to generate output string for.
        trial (Trial): Trial to generate output for.
        region (Optional[Region]): Region to generate output for.
    """
    return ','.join(
        map(lambda column: write_column(
            column, experiment, trial, region, measure, cutoff
        ), list(columns.keys()))
    ) + '\n'

def generate_region_output(experiments: List[Experiment], config_file: str = DEFAULT_CONFIG) -> str:
    """
    Generates a string in csv format of a list of experiments' region measures
    using columns specified in config file.

    Args:
        experiments (List[Experiment]): List of experiments.
        config_file (str): Name of configuration file.
    """
    config = load_config(config_file)
    measures = {key:value for (key, value) in config['region_measures'].items() if value['include']}
    columns = {key:value for (key, value) in config['region_output'].items() if value['include']}
    output = ','.join([value['header'] for value in columns.values()]) + '\n'

    for experiment in experiments:
        for trial in experiment.trials.values():
            for region in trial.item.regions:
                for (measure, value) in measures.items():
                    output += measure_output(
                        measure, value['cutoff'], columns, experiment, trial, region
                    )
    return output


def generate_trial_output(experiments: List[Experiment], config_file: str = DEFAULT_CONFIG) -> str:
    """
    Generates a string in csv format of list of experiments' trial measures using columns and
    measures specified in config file.

    Args:
        experiments (List[Experiment]): List of experiments.
        config_file (str): Name of configuration file.
    """
    config = load_config(config_file)
    measures = {key:value for (key, value) in config['trial_measures'].items() if value['include']}
    columns = {key:value for (key, value) in config['trial_output'].items() if value['include']}
    output = ','.join([value['header'] for value in columns.values()]) + '\n'

    for experiment in experiments:
        for trial in experiment.trials.values():
            for (measure, value) in measures.items():
                measure_output(measure, value['cutoff'], columns, experiment, trial, None)
    return output

def generate_all_output(experiments: List[Experiment], config_file: str = DEFAULT_CONFIG) -> str:
    """
    Generates a string in csv format of all measures specified in config file for a
    list of experiments.
    Args:
        experiments (List[Experiment]): List of experiments.
        config_file (str): Name of configuration file.
    """
    config = load_config(config_file)
    region_measures = {
        key:value for (key, value)
        in config['region_measures'].items()
        if value['include']
    }
    trial_measures = {
        key:value for (key, value)
        in config['trial_measures'].items()
        if value['include']
    }
    columns = {
        key:value for (key, value)
        in {**config['region_output'], **config['trial_output']}.items()
        if value['include']
    }
    columns = {**columns, 'measure': {'header': 'measure'}, 'value': {'header': 'value'}}

    output = ','.join([value['header'] for value in columns.values()]) + '\n'

    for experiment in experiments:
        for trial in experiment.trials.values():
            for (measure, value) in trial_measures.items():
                output += measure_output(measure, value['cutoff'], columns, experiment, trial, None)
            for region in trial.item.regions:
                for (measure, value) in region_measures.items():
                    output += measure_output(measure, value['cutoff'], columns,
                                             experiment, trial, region)
    return output

def generate_all_output_wide_format(
        experiments: List[Experiment],
        config_file: str = DEFAULT_CONFIG
) -> str:
    """
    Generates a string in csv format of all measures specified in config file for a
    list of experiments, with all measures as columns.

    Args:
        experiments (List[Experiment]): List of experiments.
        config_file (str): Name of configuration file.
    """
    config = load_config(config_file)
    columns = {
        key:value for (key, value)
        in {
            **config['region_output'],
            **config['trial_output'],
            **config['region_measures'],
            **config['trial_measures']
        }.items()
        if value['include']}
    output = ','.join([value['header'] for value in columns.values()]) + '\n'

    for experiment in experiments:
        for trial in experiment.trials.values():
            for region in trial.item.regions:
                output += ','.join(
                    map(
                        lambda column: write_column(
                            column[0],
                            experiment,
                            trial,
                            region,
                            column[0],
                            (column[1]['cutoff'] if 'cutoff' in column[1] else None)
                        ),
                        [(key, value) for (key, value) in columns.items()]
                    )
                ) + '\n'
    return output
