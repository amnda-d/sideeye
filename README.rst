========
SideEye
========
|circleci| |docs|

SideEye is still in beta! New features are in development, but if you find any bugs or have suggestions, `Open a GitHub issue <https://github.com/zediski/sideeye/issues/new/choose>`_ or email `sideeye@amnda.me <sideeye@amnda.me>`_.

SideEye is a Python package for processing eye tracking data that interfaces with EyeTrack and Experiment Builder.

It is meant to parse eye-tracking-while-reading data and calculate useful experimental measures. Currently, SideEye can only parse the .DA1 file format, but other formats will be added later. The goal is to parse all eye-tracking-while-reading data into a common format, and provide a consistent and accurate method for processing the data.

Documentation (currently incomplete, but more detail than provided here) can be found at `sideeye.readthedocs.io <http://sideeye.readthedocs.io/en/latest/index.html#>`_.

Refer to `examples/sample.py <examples/sample.py>`_ for an up-to-date sample script.

Installation
------------------

SideEye requires Python >= 3.5.

::

  pip install sideeye


Options
----------------------

The configuration file is a JSON file specifying the changeable parameters used by SideEye's default parsing and output functions. An example is found in `examples/sample_config.json <examples/sample_config.json>`_. The config file should always have the same format. It has several sections:

``da1_fields``: The locations of values in each line of a DA1 file.

``region_fields``: The locations of values in each line of a region file.

``cutoffs``: Fixation duration cutoffs.

``region_measures``: Used in region measure calculation and output.

``trial_measures``: Used in trial measure calculation and output.

``region_output``: Reported columns for region measures in output file.

``trial_output``: Reported columns for trial measures in output file.

``terminal_output``: Amount of status/debugging info to output to terminal.

da1_fields
~~~~~~~~~~

This section contains parameters needed for parsing DA1 files. Because there are several formats for DA1 files, the positions of each value in a line are needed. The parameters are all positions in a line, where 0 is the first value in the line.:

``index``: An integer identifying a single trial, usually the first number in a line.

``condition``: A value identifying the condition of the trial.

``number``: A value identifying the item of the trial.

``time``: The total time of a trial, sometimes either not included in DA1 files or at the end of every line. If this is true, this parameter should be ``-1``.

``fixation_start``: The position in a line where fixation data starts.

As an example, a line of a DA1 file could look like this:

::

  Position:   0   |   1   |   2   | 3 | 4 | 5 | 6 | 7 |   8   |   9   | ... |  -1  |
  Value:    index | cond. | num.  |   |   |   |   |   | fix.  | fix.  | ... | time |

And the ``da1_fields`` section of the config file would be:

::

  "da1_fields" : {
    "index": 0,
    "condition": 1,
    "number": 2,
    "time": -1,
    "fixation_start": 8
  }

region_fields
~~~~~~~~~~~~~

Similar to ``da1_fields``, this section specifies the positions of values in each line of a region file. The parameters are:

``number``: Item identifier.

``condition``: Item condition.

``boundaries_start``: The position where region boundaries start in a line.

``includes_y``: Whether or not the region file includes line position in region boundaries. If true, a region is bounded by four numbers: ``(char_start, line_start), (char_end, line_end)``. If false, the region is bounded by two numbers: ``char_start, char_end``.

cutoffs
~~~~~~~

This section contains cutoffs for fixations. If a fixation's duration is less than `min` or greater than `max`, it will be excluded from measure calculations.

``min``: Minimum cutoff time for fixation duration.

``max``: Maximum cutoff time for fixation duration.

``include_fixation``: When true, if a fixation is excluded by cutoffs, its duration is included in the duration of the saccade between the previous and next non-excluded fixations.

``include_saccades``: When true, if a fixation is excluded by cutoffs, the duration of the saccade into and out of the fixation is included in the saccade between the previous and next non-excluded fixations.


region_measures
~~~~~~~~~~~~~~~

This section contains parameters for region measure calculation and output. It is a list of all calculated region measure, each with two parameters:

``cutoff``: A cutoff value for the measure. If the calculated measure is greater than this value, its value in the output report is ``CUTOFF``. For some measures, where the value is not numerical, this parameter is ignored.

``include``: A boolean (true/false) value specifying whether the measure should be included in the output report. If false, the measure will be excluded.

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

``include``: Whether or not the column should be included in the output report. true/false

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

``measure``: Name of measure.

``value``: Value of measure.

trial_output
~~~~~~~~~~~~

This section specifies the columns that should be included in the output file for trial measures. Each column has the same parameters as ``region_output``. The columns are the same, but with columns beginning with ``region_`` excluded.

terminal_output
~~~~~~~~~~~~~~~

A number specifying the level of detail in terminal output.

``0``: Errors only.

``1``: File-level information (which file is currently being parsed).

``2``: Item and trial-level parsing information.

``3``: Measure-level calculation information.

``4``: Trial-level calculation information.

``5``: All output information.

.. |docs| image:: https://readthedocs.org/projects/docs/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://sideeye.readthedocs.io/en/latest/?badge=latest

.. |circleci| image:: https://circleci.com/gh/amnda-d/sideeye/tree/master.svg?style=shield
    :alt: Build Status
    :scale: 100%
    :target: https://circleci.com/gh/amnda-d/sideeye/tree/master
