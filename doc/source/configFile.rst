The Configuration File
======================

.. contents::

The configuration file is a JSON file specifying the parameters used by SideEye's parsing and output functions. There is a :doc:`default configuration <default_config.json>` used by SideEye if a custom configuration is not provided.
A custom configuration file must contain the same fields as the default configuration file. To use a custom configuration, copy :doc:`default_config.json <default_config.json>`, change values to your configuration, and provide the file name in functions requiring a configuration in your code.

The sections of the config file are:

``wide_format``: Whether the output file should be in wide or long format.

``da1_fields``: The locations of values in each line of a .DA1 file.

``region_fields``: The locations of values in each line of a region file.

``cutoffs``: Fixation duration cutoffs.

``region_measures``: Used in region measure calculation and output.

``trial_measures``: Used in trial measure calculation and output.

``region_output``: Reported columns for region measures in output file.

``trial_output``: Reported columns for trial measures in output file.

``terminal_output``: Amount of status/debugging information to output to terminal.

wide_format
~~~~~~~~~~~

A boolean (``true/false``) indicating whether the output should be in wide or long format. If ``true``, the output will be in wide format, with each measure as a column of the csv. If ``false``, the output will be in long format, with each measure as a separate row of the csv.

For example, the column headers in long format will be:

::

  experiment_name,trial_id,trial_total_time,item_id,item_condition,region_number,measure,value

The column headers in wide format will be:

::
  experiment_name,trial_id,trial_total_time,item_id,item_condition,region_number,skip,first_pass_regressions_out, ... ,average_forward_saccade,average_backward_saccade

da1_fields
~~~~~~~~~~

This section contains parameters needed for parsing .DA1 files. A .DA1 file describes the position and timing of fixations. Each line of the file represents a single trial in an experiment. The first fields in the line contain information identifying the trial. After these fields, fixations are represented by groups of four numbers - x-position, y-position, start time, and end time. Five fields are necessary for parsing a .DA1 file:

``index``: An integer identifying a single trial, usually the first number in the line.

``condition``: A value identifying the condition of the trial.

``number``: A value identifying the item of the trial.

``time``: The total time of a trial, sometimes either not included in DA1 files or at the end of every line. If this is true, this parameter should be ``-1``.

``fixation_start``: The position in a line where fixation data starts.

The default configuration for .DA1 files is:

::

  "da1_fields" : {
    "index": 0,
    "condition": 1,
    "number": 2,
    "time": -1,
    "fixation_start": 8
  }

This default configuration matches a .DA1 file with the following format:

::

  Position:   0   |   1   |   2   | 3 | 4 | 5 | 6 | 7 |   8   |   9   | ... |  -1  |
  ----------------------------------------------------------------------------------
  Value:    index | cond. | num.  |   |   |   |   |   | fix.  | fix.  | ... | time |

region_fields
~~~~~~~~~~~~~

Similar to ``da1_fields``, this section specifies the positions of values in each line of a region file. If the newer text region format is used, this section of the configuration is ignored. Region files (typically .cnt or .reg) describe regions of interest in items of the experiment. Regions are defined by a character position of the beginning and ending of the region. Character positions can either be a single integer for single-line items, or a pair (line, character) of integers for multi-line items. A line in a region file contains the number and condition of an item, followed by the beginning and end positions of the regions. Four fields are necessary for parsing a region file.

``number``: Item identifier.

``condition``: Item condition.

``boundaries_start``: The position where region boundaries start in a line.

``includes_y``: True for multi-line items where regions are bounded by character and line position pairs, false for single-line items where regions are bounded by single integer character positions.

The default configuration for region files is:

::

  "region_fields": {
    "number": 0,
    "condition": 1,
    "boundaries_start": 3,
    "includes_y": false
  }

The default configuration matches a region file with the following format:

::

  Position:   0   |   1   | 2 |   3   |   4   |   5   |   6   | ... |
  -------------------------------------------------------------------
  Value:    num.  | cond. |   |  r1   |  r1   |  r2   |  r2   | ... |

cutoffs
~~~~~~~

This section contains cutoffs for fixations. If a fixation's duration is less than `min` or greater than `max`, it will be excluded from measure calculations. `include_fixation` and `include_saccades` describe how excluded fixations should be handled when calculating saccades. For more information, see the examples in :ref:`Trials <Trial>`.

``min``: Minimum cutoff time for fixation duration.

``max``: Maximum cutoff time for fixation duration.

``include_fixation``: When true, if a fixation is excluded by cutoffs, its duration is included in the duration of the saccade between the previous and next non-excluded fixations.

``include_saccades``: When true, if a fixation is excluded by cutoffs, the duration of the saccade into and out of the fixation is included in the saccade between the previous and next non-excluded fixations.

region_measures
~~~~~~~~~~~~~~~

This section contains parameters for region measure calculation and output. It is a list of all calculated region measure, each with two parameters:

``cutoff``: A cutoff value for the measure. If the calculated measure is greater than this value, its value in the output report is ``CUTOFF``. For some measures, where the value is not numerical, this parameter is ignored.

``include``: A boolean (true/false) value specifying whether the measure should be included in the output report. If false, the measure will be excluded.

``header``: A string used as a header for the measure in wide output format.

The measures in this section of the config file are:

::

  skip
  first_pass_regressions_out
  first_pass_regressions_in
  first_fixation_duration
  single_fixation_duration
  first_pass
  go_past
  total_time
  right_bounded_time
  reread_time
  second_pass
  spillover_time
  refixation_time
  landing_position
  launch_site
  first_pass_fixation_count
  go_back_time_region
  go_back_time_char

trial_measures
~~~~~~~~~~~~~~

This section contains parameters for trial measure calculation and output. Each measure has the same parameters as ``region_measures``. The measures included in this section are:

::

  location_first_regression
  latency_first_regression
  fixation_count
  percent_regressions
  trial_total_time
  average_forward_saccade
  average_backward_saccade

region_output
~~~~~~~~~~~~~

This section specifies the columns that should be included in the output file for region measures. Each output column has two parameters:

``include``: Whether or not the column should be included in the output report, true or false.

``header``: A title for the header of the column. Can be different from the name of the column parameter.

Columns included in this section are:

``experiment_name``: Name of experiment.

``filename``: Filename of DA1 file.

``date``: Date of DA1 file if specified, or date file was parsed if not.

``trial_id``: Trial identifier.

``trial_total_time``: Total time of trial.

``item_id``: Item identifier.

``item_condition``: Condition of item.

``region_label``: Label for region.

``region_number``: Region number (beginning with 0).

``region_text``: Text included in region, if specified.

``region_start``: Character location of beginning of region.

``region_end``: Character location of end of region.

trial_output
~~~~~~~~~~~~

This section specifies the columns that should be included in the output file for trial measures. Each column has the same parameters as ``region_output``. The columns are the same, but with columns beginning with ``region_`` excluded.

terminal_output
~~~~~~~~~~~~~~~

A number specifying the level of detail in terminal output. This option is useful for debugging, for example, finding out if an error is being caused by a specific input file, or by calculating a specific measure.

``0``: Errors only.

``1``: File-level information (which file is currently being parsed).

``2``: Item and trial-level parsing information.

``3``: Measure-level calculation information.

``4``: Trial-level calculation information.

``5``: All output information.
