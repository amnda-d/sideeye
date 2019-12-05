"""
Functions for parsing sideeye configurations from JSON files, and
validating sideeye configuration dictionaries.
"""

import json
from typing import Dict, Union, Any


def validate_key(config_dict: Dict[str, Any], key: str, value_type: type, default: Any):
    """
    Returns config_dict[key] if the value exists and if of type value_type,
    otherwise returns a default value.
    """
    return (
        config_dict[key]
        if key in config_dict and isinstance(config_dict[key], value_type)
        else default
    )


class DA1Config:
    """
    DA1 parser configuration.

    Attributes:
        index (int): Trial index column.
        condition (int): Item condition column.
        number (int): Item number column.
        time (int): Total trial time column.
        fixation_start (int): Column number of first fixation

    Args:
        da1_config (Dict): DA1 configuration dictionary.
    """

    index: int
    condition: int
    number: int
    time: int
    fixation_start: int

    def __init__(self, da1_config: Dict[str, int] = {}):
        self.index = validate_key(da1_config, "index", int, 0)
        self.condition = validate_key(da1_config, "condition", int, 1)
        self.number = validate_key(da1_config, "number", int, 2)
        self.time = validate_key(da1_config, "time", int, -1)
        self.fixation_start = validate_key(da1_config, "fixation_start", int, 8)


class RegionConfig:
    """
    Region parser configuration.

    Attributes:
        number (int): Item number column.
        condition (int): Condition label column.
        boundaries_start (int): First region boundary column position.
        includes_y (bool): Whether or not y values are included in the region file.

    Args:
        region_config (Dict): Region configuration dictionary.
    """

    number: int
    condition: int
    boundaries_start: int
    includes_y: bool

    def __init__(self, region_config: Dict[str, Union[int, bool]] = {}):
        self.number = validate_key(region_config, "number", int, 0)
        self.condition = validate_key(region_config, "condition", int, 1)
        self.boundaries_start = validate_key(region_config, "boundaries_start", int, 3)
        self.includes_y = validate_key(region_config, "includes_y", bool, False)


class ASCParsingConfig:
    """
    ASC parser configuration.

    Attributes:
        fixation_min_cutoff (Union[int, bool]): Minimum cutoff for including a fixation.
        max_saccade_dur (Union[int, bool]): Maximum cutoff for saccade duration.
        blink_max_count (Union[int, bool]): Maximum number of blinks before trial exclusion.
        blink_max_dur (Union[int, bool])j: Maximum blink duration before trial exclusion.

    Args:
        asc_config (Dict): ASC configuration dictionary.
    """

    fixation_min_cutoff: Union[int, bool]
    max_saccade_dur: Union[int, bool]
    blink_max_count: Union[int, bool]
    blink_max_dur: Union[int, bool]

    def __init__(self, asc_config: Dict[str, Union[int, bool]] = {}):
        self.fixation_min_cutoff = validate_key(
            asc_config, "fixation_min_cutoff", int, False
        )
        self.max_saccade_dur = validate_key(asc_config, "max_saccade_dur", int, False)
        self.blink_max_count = validate_key(asc_config, "blink_max_count", int, False)
        self.blink_max_dur = validate_key(asc_config, "blink_max_dur", int, False)


class CutoffsConfig:
    """
    Fixation cutoff configuration.

    Attributes:
        min (int): Minimum cutoff for fixations.
        max (int): Maximum cutoff for fixations.
        include_fixation (bool): Whether excluded fixations should be included in saccade duration.
        include_saccades (bool): Whether the saccades into and out of an excluded
            fixation should be included in saccade duration.

    Args:
        cutoffs (dict): Cutoff configuration dictionary.
    """

    min: int
    max: int
    include_fixation: bool
    include_saccades: bool

    def __init__(self, cutoffs: Dict[str, Union[int, bool]] = {}):
        self.min = validate_key(cutoffs, "min", int, -1)
        self.max = validate_key(cutoffs, "max", int, -1)
        self.include_fixation = validate_key(cutoffs, "include_fixation", bool, False)
        self.include_saccades = validate_key(cutoffs, "include_saccades", bool, False)


class MeasuresConfig:
    """
    Region measure configuration.

    Attributes:
        region (Dict[str, OutputColumnConfig]): Output configuration for region measures.
        trial (Dict[str, OutputColumnConfig]): Output configuration for trial measures.
        all (Dict[str, OutputColumnConfig]): Output configuration for all measures.
        names (List[str]): List of all measure names.

    Args:
        region_measures (Dict[str, Dict]): Region measure configuration dictionary.
        trial_measures (Dict[str, Dict]): Trial measure configuration dictionary.
    """

    def __init__(
        self,
        region_measures: Dict[str, Dict[str, Union[int, str]]],
        trial_measures: Dict[str, Dict[str, Union[int, str]]],
    ):
        self.region = {
            measure: OutputColumnConfig(measure, config)
            for (measure, config) in region_measures.items()
            if not ("exclude" in config and config["exclude"])
        }
        self.trial = {
            measure: OutputColumnConfig(measure, config)
            for (measure, config) in trial_measures.items()
            if not ("exclude" in config and config["exclude"])
        }
        self.all = {**self.trial, **self.region}
        self.names = {**trial_measures, **region_measures}.keys()


class OutputColumnConfig:
    """
    Configuration for a single output column.

    Attributes:
        cutoff (int): Cutoff for excluding measure from output.
        header (str): Name of column in output file.

    Args:
        measure (str): Name of measure.
        measure_config (Dict): Measure configuration dictionary.
    """

    cutoff: int
    header: str

    def __init__(self, measure: str, measure_config: Dict[str, Union[int, str]] = {}):
        self.cutoff = validate_key(measure_config, "cutoff", int, None)
        self.header = validate_key(measure_config, "header", str, measure)


class OutputConfig:
    """Output column configuration."""

    def __init__(
        self,
        region_output: Dict[str, Dict[str, Union[int, str]]],
        trial_output: Dict[str, Dict[str, Union[int, str]]],
    ):
        self.region = {
            measure: OutputColumnConfig(measure, config)
            for (measure, config) in region_output.items()
            if not ("exclude" in config and config["exclude"])
        }
        self.trial = {
            measure: OutputColumnConfig(measure, config)
            for (measure, config) in trial_output.items()
            if not ("exclude" in config and config["exclude"])
        }
        self.columns = {**self.region, **self.trial}


class Configuration:
    """
    SideEye configuration.

    Attributes:
        wide_format (bool): Whether output should be in wide (True) or long (False) format.
        da1_fields (DA1Config): DA1 file configuration.
        region_fields (RegionConfig): Region file configuration.
        asc_parsing (ASCParsingConfig): ASC file configuration.
        cutoffs (CutoffsConfig): Fixation cutoff configuration.
        measures (MeasuresConfig): Configuration for calculating measures.
        output (OutputConfig): Output file configuration.
        terminal_output (int): Verbose output level.

    Args:
        config_file (Optional[str]): Path to configuration JSON file.
    """

    wide_format: bool
    da1_fields: DA1Config
    region_fields: RegionConfig
    asc_parsing: ASCParsingConfig
    cutoffs: CutoffsConfig
    measures: MeasuresConfig
    output: OutputConfig
    terminal_output: int

    def __init__(self, config_file: str = None):
        config: Dict = {}
        if config_file:
            with open(config_file) as cfg:
                config = json.load(cfg)
        self.wide_format = config["wide_format"] if "wide_format" in config else True
        self.da1_fields = DA1Config(
            config["da1_fields"] if "da1_fields" in config else {}
        )
        self.region_fields = RegionConfig(
            config["region_fields"] if "region_fields" in config else {}
        )
        self.asc_parsing = ASCParsingConfig(
            config["asc_parsing"] if "asc_parsing" in config else {}
        )
        self.cutoffs = CutoffsConfig(config["cutoffs"] if "cutoffs" in config else {})
        self.measures = MeasuresConfig(
            config["region_measures"]
            if "region_measures" in config
            else {
                "skip": {},
                "first_pass_regressions_out": {},
                "first_pass_regressions_in": {},
                "first_fixation_duration": {},
                "single_fixation_duration": {},
                "first_pass": {},
                "go_past": {},
                "total_time": {},
                "right_bounded_time": {},
                "reread_time": {},
                "second_pass": {},
                "spillover_time": {},
                "refixation_time": {},
                "landing_position": {},
                "launch_site": {},
                "first_pass_fixation_count": {},
                "go_back_time_region": {},
                "go_back_time_char": {},
            },
            config["trial_measures"]
            if "trial_measures" in config
            else {
                "location_first_regression": {},
                "latency_first_regression": {},
                "fixation_count": {},
                "percent_regressions": {},
                "trial_total_time": {},
                "average_forward_saccade": {},
                "average_backward_saccade": {},
            },
        )
        self.output = OutputConfig(
            config["region_output"]
            if "region_output" in config
            else {
                "experiment_name": {},
                "filename": {"exclude": True, "header": "filename"},
                "date": {"exclude": True, "header": "date"},
                "trial_id": {},
                "trial_total_time": {},
                "item_id": {},
                "item_condition": {},
                "region_label": {"exclude": True, "header": "region_label"},
                "region_number": {},
                "region_text": {"exclude": True, "header": "region_text"},
                "region_start": {"exclude": True, "header": "region_start"},
                "region_end": {"exclude": True, "header": "region_end"},
            },
            config["trial_output"]
            if "trial_output" in config
            else {
                "experiment_name": {},
                "filename": {"exclude": True, "header": "filename"},
                "date": {"exclude": True, "header": "date"},
                "trial_id": {},
                "trial_total_time": {},
                "item_id": {},
                "item_condition": {},
            },
        )
        self.terminal_output = (
            config["terminal_output"] if "terminal_output" in config else 0
        )
