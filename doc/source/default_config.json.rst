Default Configuration
=====================

::

  {
    "wide_format": true,
    "da1_fields": {
      "index": 0,
      "condition": 1,
      "number": 2,
      "time": -1,
      "fixation_start": 8
    },
    "region_fields": {
      "number": 0,
      "condition": 1,
      "boundaries_start": 3,
      "includes_y": false
    },
    "asc_parsing": {
      "fixation_min_cutoff": false,
      "max_saccade_dur": false,
      "blink_max_count": false,
      "blink_max_dur": false
    },
    "cutoffs": {
      "min": -1,
      "max": -1,
      "include_fixation": false,
      "include_saccades": false
    },
    "region_measures": {
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
      "go_back_time_char": {}
    },
    "trial_measures": {
      "location_first_regression": {},
      "latency_first_regression": {},
      "fixation_count": {},
      "percent_regressions": {},
      "trial_total_time": {},
      "average_forward_saccade": {},
      "average_backward_saccade": {}
    },
    "output_columns": {
      "experiment_name": {},
      "filename": { "exclude": true },
      "date": { "exclude": true },
      "trial_id": {},
      "trial_total_time": {},
      "item_id": {},
      "item_condition": {},
      "region_label": { "exclude": true },
      "region_number": {},
      "region_text": { "exclude": true },
      "region_start": { "exclude": true },
      "region_end": { "exclude": true }
    },
    "terminal_output": 0
  }
