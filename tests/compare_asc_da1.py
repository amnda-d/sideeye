import os
import sys
import sideeye

DIRNAME = os.path.dirname(os.path.realpath(__file__))
REGION_FILE = sys.argv[1]
DA1 = sys.argv[2]
ASC = sys.argv[3]
CONFIG = sys.argv[4]

ITEMS = sideeye.parser.region.file(REGION_FILE, sideeye.config.Configuration(CONFIG))

DA1_EXPERIMENT = sideeye.parser.experiment.parse(
    DA1, REGION_FILE, sideeye.config.Configuration(CONFIG)
)
ASC_EXPERIMENT = sideeye.parser.asc.parse(
    ASC, ITEMS, sideeye.config.Configuration(CONFIG).asc_parsing
)

if DA1_EXPERIMENT != ASC_EXPERIMENT:
    for key, da1_trial in DA1_EXPERIMENT.trials.items():
        asc_trial = ASC_EXPERIMENT.trials[key]
        if asc_trial != da1_trial:
            print("\nASC TRIAL\n-----------------------------------------")
            print(asc_trial)
            print("\nDA1 TRIAL\n-----------------------------------------")
            print(da1_trial)
            print("\n")
