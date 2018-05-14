"""
This module contains functions to generate csv reports of measures calculated
for experiments.
"""

import json

def load_config(config_file):
# Load a JSON config file into a dictionary.
    with open(config_file) as cfg:
        return json.load(cfg)

def write_column(column, experiment, trial, region, measure, cutoff):
# Map a column name to an output value.
    output = 'NA'
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
        if region is not None:
            output = trial.region_measures[region.number][measure]['value']
        else:
            output = trial.trial_measures[measure]
        if cutoff >= 0 and isinstance(output, int) and output > cutoff:
            output = 'CUTOFF'
    else:
        raise ValueError('Column %s is not defined' % column)
    return str(output)

def measure_output(measure, cutoff, columns, experiment, trial, region):
    """
    Generates a formatted output string for an individual measure.

    Args:
        measure (str): Name of measure.
        cutoff (int): Cutoff value for measure. Use -1 for no cutoff.
        columns (List[str]): List of columns to output.
        experiment (Experiment): Experiment to generate output string for.
        trial (Trial): Trial to generate output for.
        region (Region): Region to generate output for.
    """
    return ','.join(map(lambda column: write_column(column, experiment, trial,
                                                    region, measure, cutoff),
                        list(columns.keys()))) + '\n'

def generate_region_output(experiments, config_file='sideeye/default_config.json'):
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
                    output += measure_output(measure, value['cutoff'], columns,
                                             experiment, trial, region)
    return output


def generate_trial_output(experiments, config_file='sideeye/default_config.json'):
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

def generate_all_output(experiments, config_file='sideeye/default_config.json'):
    """
    Generates a string in csv format of all measures specified in config file for a
    list of experiments.

    Args:
        experiments (List[Experiment]): List of experiments.
        config_file (str): Name of configuration file.
    """
    config = load_config(config_file)
    region_measures = {key:value for (key, value)
                       in config['region_measures'].items()
                       if value['include']}
    trial_measures = {key:value for (key, value)
                      in config['trial_measures'].items()
                      if value['include']}
    columns = {key:value for (key, value)
               in {**config['region_output'], **config['trial_output']}.items()
               if value['include']}
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
