Data
=====================

.. contents::

.. automodule:: sideeye.data

.. _Experiment:

Experiment
--------------------------------

An Experiment is the highest-level data object in the SideEye module, representing a single participant's data.

.. autoclass:: sideeye.data.Experiment
  :members:

.. _Trial:

Trial
---------------------------

A Trial represents the data from a participant reading one item. An individual Trial is identified by an index, and contains the total time spent reading the Item, lists of Fixations and Saccades associated with the Trial, and a dictionary of trial and region measures calculated for the Trial.

The list of saccades for a Trial is generated using the list of fixations. There are two parameters that affect how saccades are defined: `include_fixation` and `include_saccades`. If a Fixation is excluded from calculations, there are several ways to define a saccade. If `include_fixation` is true, the excluded fixation will be included in the duration of the Saccade. If `include_saccades` is true, the saccades surrounding an excluded fixation are included in the duration of the Saccade.

In the following example, the excluded fixation and surrounding saccades are included in the Saccade, which has a total duration of 30ms.

::

  include_saccades: True
  include_fixations: True

  Time:      0        10      20           30      40       50
  Fixations: |  fix1  |       | excl. fix. |       |  fix3  |
             ------------------------------------------------
  Saccades:  |        |          saccade1          |        |

  Trial.fixations = [fix1, fix2]
  Trial.saccades = [saccade1]

If the excluded fixation is included in the saccade, but the surrounding saccades are not, the Saccade has a total duration of 10ms.

::

  include_saccades: False
  include_fixations: True

  Time:      0        10      20           30      40       50
  Fixations: |  fix1  |       | excl. fix. |       |  fix3  |
             ------------------------------------------------
  Saccades:  |                |  saccade1  |                |

  Trial.fixations = [fix1, fix3]
  Trial.saccades = [saccade1]

If the surrounding saccades are included, but the excluded fixation is not, the total duration of the Saccade is 20ms - the sum of the durations of the two surrounding saccades.

::

  include_saccades: True
  include_fixations: False

  Time:      0        10      20           30      40       50
  Fixations: |  fix1  |       | excl. fix. |       |  fix3  |
             ------------------------------------------------
  Saccades:  |        | sacc1 |  EXCLUDED  | sacc1 |        |

  Trial.fixations = [fix1, fix3]
  Trial.saccades = [sacc1(both parts combined)]

If the excluded fixation and surrounding saccades are both not included, no Saccade is added to the Trial. This is the default.

::

  include_saccades: False
  include_fixations: False

  Time:      0        10      20           30      40       50
  Fixations: |  fix1  |       | excl. fix. |       |  fix3  |
             ------------------------------------------------
  Saccades:  |        |          EXCLUDED          |        |

  Trial.fixations = [fix1, fix3]
  Trial.saccades = []

The Trial object also contains all measures that have been calculated so far. `trial_measures` is a dictionary mapping measure names to calculation outputs. `region_measures` is a dictionary mapping region numbers to dictionaries mapping measure names to calculation outputs. Region measure outputs are in the format `{'value': output_value, 'fixations': fixation_in_calculation}`:

::

  trial_measures = {
    'measure_1': False,
    'measure_2': 5000,
    ...
  }

  region_measures = {
    0: {
      'region_measure_1': {'value': 50, 'fixations': [fix1, fix3]},
      'region_measure_2': {'value': True, 'fixations': [fix4]},
      ...
    },
    1: {
    'region_measure_1': {'value': 148, 'fixations': [fix2, fix5, fix6]},
    'region_measure_2': {'value': False, 'fixations': None},
      ...
    },
    ...
  }

.. autoclass:: sideeye.data.Trial
  :members:

.. _Item:

Item
--------------------------

An Item represents the text that is displayed to a participant during a trial. A number and condition identify the item, which consists of a list of regions, and optionally a list of labels for the regions.

.. autoclass:: sideeye.data.Item
  :members:

.. _Region:

Region
----------------------------

A Region represents the boundaries of a region in an Item as (character, line) points in the text of the Item. A region also has a label, number, and optionally the text contained in the region.

.. autoclass:: sideeye.data.Region
  :members:

.. _Saccade:

Saccade
-----------------------------

A Saccade is the period of time between two fixations. The start of the Saccade is the Fixation before the Saccade, and the end is the Fixation after the Saccade. If the location of the end Fixation is earlier in the Item the location of the start Fixation, the Saccade is a regression.

.. autoclass:: sideeye.data.Saccade
  :members:

.. _Fixation:

Fixation
------------------------------

A Fixation represents a period of time where a participant fixated on an item in a trial. Fixation position is represented by character and line position in the item. A Fixation can also hold information about the region of the item it occurred in, and whether or not it has been excluded by fixation cutoff parameters.

.. autoclass:: sideeye.data.Fixation
  :members:

.. _Point:

Point
---------------------------

A Point represents an (x, y) location. It is used to represent fixation positions and region boundaries.

.. autoclass:: sideeye.data.Point
  :members:
