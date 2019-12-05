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
import os
import sideeye

# Get directory path.
DIRNAME = os.path.dirname(os.path.realpath(__file__))

# Get config file path.
CONFIG = sideeye.config.Configuration(os.path.join(DIRNAME, "sample_config.json"))

# Parse all DA1 files in directory using items listed in region file.
EXPERIMENTS = sideeye.parser.experiment.parse_files(
    [
        os.path.join(os.path.join(DIRNAME, "sample_DA1s"), da1)
        for da1 in os.listdir(os.path.join(DIRNAME, "sample_DA1s"))
    ],
    os.path.join(DIRNAME, "sample.cnt"),
    CONFIG,
)

# Calculate all measures listed in config file, and output results as a csv.
sideeye.calculate_all_measures(EXPERIMENTS, "sample_output.csv", CONFIG)
