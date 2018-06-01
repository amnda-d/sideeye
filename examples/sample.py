"""
This is an example of how to use the SideEye module in a simple way. It takes a
directory of DA1 files (examples/sample_DA1s), a region file (examples/sample.cnt),
and a config file (examples/sample_config.json) as input. The DA1 files are parsed
into a list SideEye experiment objects, and all measures specified in the config
file are calculated and output as a csv file (examples/sample_output.csv).

To run: Copy this file and sample_config.json into a directory containing a
region file and a directory of DA1 files. Edit the file names below to match your files,
and make any necessary changes to the config file. Run sample.py in the new directory.
"""

# Import modules.
import sideeye
import os

# Get directory path.
dirname = os.path.dirname(os.path.realpath(__file__))

# Get config file path.
config = os.path.join(dirname, 'sample_config.json')

# Parse all DA1 files in directory using items listed in region file.
experiments = sideeye.parser.experiment.parse_dir(os.path.join(dirname, 'sample_DA1s'), os.path.join(dirname, 'sample.cnt'), config)

# Calculate all measures listed in config file, and output results as a csv.
sideeye.calculate_all_measures(experiments, 'sample_output.csv', config)
