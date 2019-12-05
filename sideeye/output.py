"""
This module contains functions to generate csv reports of measures calculated
for experiments.
"""

from typing import Any, List, Dict, Optional
from sideeye.data import Experiment, Trial, Region
from sideeye.config import Configuration, OutputColumnConfig


def write_column(
    column: str,
    experiment: Experiment,
    trial: Trial,
    region: Optional[Region],
    measure: str,
    cutoff: int,
) -> str:
    """Maps a column name to an output value."""
    output: Any = "NA"
    if column == "experiment_name":
        output = experiment.name
    elif column == "filename":
        output = experiment.filename
    elif column == "date":
        output = experiment.date
    elif column == "trial_id":
        output = trial.index
    elif column == "trial_total_time":
        output = trial.time
    elif column == "item_id":
        output = trial.item.number
    elif column == "item_condition":
        output = trial.item.condition
    elif column == "region_label":
        if region is not None:
            output = region.label
    elif column == "region_number":
        if region is not None:
            output = region.number
    elif column == "region_text":
        if region is not None:
            output = f'"{region.text}"'
    elif column == "region_start":
        if region is not None:
            output = f'"{region.start}"'
    elif column == "region_end":
        if region is not None:
            output = f'"{region.end}"'
    elif column == "measure":
        output = f'"{measure}"' if "," in str(measure) else measure
    elif (
        region is not None
        and region.number is not None
        and measure in trial.region_measures[region.number]
    ):
        output = trial.region_measures[region.number][measure]["value"]
    elif measure in trial.trial_measures:
        output = trial.trial_measures[measure]
    if isinstance(output, int) and cutoff and output > cutoff >= 0:
        output = "CUTOFF"
    return str(output).replace("\n", "\\n")


def measure_output(
    measure: str,
    cutoff: int,
    columns: Dict[str, OutputColumnConfig],
    experiment: Experiment,
    trial: Trial,
    region: Optional[Region],
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
    return (
        ",".join(
            map(
                lambda column: write_column(
                    column, experiment, trial, region, measure, cutoff
                ),
                list(columns.keys()),
            )
        )
        + "\n"
    )


def generate_region_output(
    experiments: List[Experiment], config: Configuration = Configuration()
) -> str:
    """
    Generates a string in csv format of a list of experiments' region measures
    using columns specified in config file.

    Args:
        experiments (List[Experiment]): List of experiments.
        config (Configuration): Configuration.
    """
    measures = config.measures.region
    columns = config.output.region
    output = ",".join([value.header for value in columns.values()]) + "\n"

    for experiment in experiments:
        for trial in experiment.trials.values():
            for region in trial.item.regions:
                for (measure, value) in measures.items():
                    output += measure_output(
                        measure, value.cutoff, columns, experiment, trial, region
                    )
    return output


def generate_trial_output(
    experiments: List[Experiment], config: Configuration = Configuration()
) -> str:
    """
    Generates a string in csv format of list of experiments' trial measures using columns and
    measures specified in config file.

    Args:
        experiments (List[Experiment]): List of experiments.
        config (Configuration): Configuration.
    """
    measures = config.measures.trial
    columns = config.output.trial
    output = ",".join([value.header for value in columns.values()]) + "\n"

    for experiment in experiments:
        for trial in experiment.trials.values():
            for (measure, value) in measures.items():
                measure_output(measure, value.cutoff, columns, experiment, trial, None)
    return output


def generate_all_output(
    experiments: List[Experiment], config: Configuration = Configuration()
) -> str:
    """
    Generates a string in csv format of all measures specified in config file for a
    list of experiments.
    Args:
        experiments (List[Experiment]): List of experiments.
        config (Configuration): Configuration.
    """
    region_measures = config.measures.region
    trial_measures = config.measures.trial
    columns = config.output.columns

    output = ",".join([value.header for value in columns.values()]) + "\n"

    for experiment in experiments:
        for trial in experiment.trials.values():
            for (measure, value) in trial_measures.items():
                output += measure_output(
                    measure, value.cutoff, columns, experiment, trial, None
                )
            for region in trial.item.regions:
                for (measure, value) in region_measures.items():
                    output += measure_output(
                        measure, value.cutoff, columns, experiment, trial, region
                    )
    return output


def generate_all_output_wide_format(
    experiments: List[Experiment], config: Configuration = Configuration()
) -> str:
    """
    Generates a string in csv format of all measures specified in config file for a
    list of experiments, with all measures as columns.

    Args:
        experiments (List[Experiment]): List of experiments.
        config (Configuration): Configuration.
    """
    columns: Dict[str, OutputColumnConfig] = {
        **config.output.columns,
        **config.measures.all,
    }
    output = ",".join([value.header for value in columns.values()]) + "\n"

    for experiment in experiments:
        for trial in experiment.trials.values():
            for region in trial.item.regions:
                output += (
                    ",".join(
                        map(
                            lambda col: write_column(
                                col[0],
                                experiment,
                                trial,
                                region,
                                col[0],
                                col[1].cutoff,  # pylint: disable=no-member
                            ),
                            columns.items(),
                        )
                    )
                    + "\n"
                )
    return output
