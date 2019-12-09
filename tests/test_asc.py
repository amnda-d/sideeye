import os
from nose2.tools import such
from sideeye import config, parser, Point, Fixation, Trial, Item

with such.A(".ASC Parser") as it:

    @it.has_setup
    def setup():
        it.asc_header = """
        MSG 1 SYNCTIME
        MSG 1000 TRIALID E1I1D0
        MSG 1001 REGION CHAR 1 1 T 10 100 20 110
        MSG 1002 REGION CHAR 1 1 e 20 100 30 110
        MSG 1003 REGION CHAR 1 1 s 30 100 40 110
        MSG 1004 REGION CHAR 1 1 t 40 100 50 110
        MSG 1005 REGION CHAR 1 1   50 100 60 110
        MSG 1006 REGION CHAR 1 1 i 60 100 70 110
        MSG 1007 REGION CHAR 1 1 t 70 100 80 110
        MSG 1008 REGION CHAR 1 1 e 80 100 90 110
        MSG 1009 REGION CHAR 1 1 m 90 100 100 110
        """
        it.asc_end = """
        MSG 10001 TRIAL_RESULT 7
        MSG 10002 TRIAL OK
        """
        it.items = {"1": {"1": Item("1", "1", parser.region.text("Test/ item"))}}

    @it.should("given a .ASC file, return an Experiment object")
    def test_exp():
        experiment = parser.asc.parse(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "testdata/test.asc"
            ),
            it.items,
        )
        it.assertEqual(experiment.name, "test")
        it.assertTrue("testdata/test.asc" in experiment.filename)

    @it.should("given a list of items, parse a .ASC file with one fixation")
    def test_asc():
        fixation = "EFIX R 2000 2010 10 12 105 0"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixation + it.asc_end, it.items
        )
        it.assertEqual(len(parsed_experiment), 1)
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [Fixation(Point(0, 0), 0, 10, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should("given a list of items, parse a .ASC file with two trials")
    def test_2_asc():
        trial_1 = it.asc_header + "EFIX R 2000 2010 10 12 105 0" + it.asc_end
        trial_2 = """
        MSG 20000 SYNCTIME
        MSG 20000 TRIALID E1I1D0
        MSG 20001 REGION CHAR 1 1 T 10 100 20 110
        MSG 20002 REGION CHAR 1 1 e 20 100 30 110
        MSG 20003 REGION CHAR 1 1 s 30 100 40 110
        MSG 20004 REGION CHAR 1 1 t 40 100 50 110
        MSG 20005 REGION CHAR 1 1   50 100 60 110
        MSG 20006 REGION CHAR 1 1 i 60 100 70 110
        MSG 20007 REGION CHAR 1 1 t 70 100 80 110
        MSG 20008 REGION CHAR 1 1 e 80 100 90 110
        MSG 20009 REGION CHAR 1 1 m 90 100 100 110
        EFIX R 30000 30010 10 12 105 0
        MSG 40000 TRIAL_RESULT 7
        MSG 40001 TRIAL OK
        """
        parsed_experiment = parser.asc.get_trials(trial_1 + trial_2, it.items)
        it.assertEqual(len(parsed_experiment), 2)
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [Fixation(Point(0, 0), 0, 10, 0, it.items["1"]["1"].regions[0])],
            ),
        )
        it.assertEqual(
            parsed_experiment[1],
            Trial(
                1,
                20000,
                it.items["1"]["1"],
                [Fixation(Point(0, 0), 0, 10, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should("only parse trials ending in D0")
    def test_d0_d1():
        trial_1 = it.asc_header + "EFIX R 2000 2010 10 12 105 0" + it.asc_end
        trial_2 = """
        MSG 20000 SYNCTIME
        MSG 20000 TRIALID E1I1D1
        MSG 20001 REGION CHAR 1 1 A 10 100 20 110
        MSG 20002 REGION CHAR 1 1 a 20 100 30 110
        MSG 20003 REGION CHAR 1 1 a 30 100 40 110
        MSG 20004 REGION CHAR 1 1 a 40 100 50 110
        EFIX R 30000 30010 10 12 105 0
        MSG 40000 TRIAL_RESULT 7
        MSG 40001 TRIAL OK
        """
        parsed_experiment = parser.asc.get_trials(trial_1 + trial_2, it.items)
        it.assertEqual(len(parsed_experiment), 1)
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [Fixation(Point(0, 0), 0, 10, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should("given a list of items, parse a .ASC file with multiple fixations")
    def test_multifix_da1():
        fixation = "EFIX R 2000 2010 10 12 105 0\nEFIX R 2010 2030 20 72 105 0"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixation + it.asc_end, it.items
        )
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [
                    Fixation(Point(0, 0), 0, 10, 0, it.items["1"]["1"].regions[0]),
                    Fixation(Point(6, 0), 10, 30, 1, it.items["1"]["1"].regions[1]),
                ],
            ),
        )

    @it.should("not exclude trials with blinks shorter than blink_max_dur")
    def test_short_blinks():
        fixation = "EFIX R 2000 2010 10 12 105 0\nEBLINK R 2010 2015 5"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixation + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": 20,
                    "blink_max_count": False,
                    "max_saccade_dur": False,
                    "fixation_min_cutoff": False,
                }
            ),
        )
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [Fixation(Point(0, 0), 0, 10, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should("exclude trials with blinks longer than blink_max_dur")
    def test_long_blinks():
        fixation = "EFIX R 2000 2010 10 12 105 0\nEBLINK R 2010 2050 40"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixation + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": 20,
                    "blink_max_count": False,
                    "max_saccade_dur": False,
                    "fixation_min_cutoff": False,
                }
            ),
        )
        it.assertEqual(parsed_experiment, [])

    @it.should("exclude trials with more blinks than max_blink_count")
    def test_many_blinks():
        fixation = "EFIX R 2000 2010 10 12 105 0\nEBLINK R 2010 2020 10\nEBLINK R 2020 2030 10\n"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixation + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": False,
                    "blink_max_count": 1,
                    "max_saccade_dur": False,
                    "fixation_min_cutoff": False,
                }
            ),
        )
        it.assertEqual(parsed_experiment, [])

    @it.should(
        "merge a fixation shorter than fixation_min_cutoff with the previous fixation"
    )
    def test_fix_merge():
        fixations = "EFIX R 2000 2020 20 12 105 0\nEFIX R 2020 2025 5 33 105 0"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixations + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": False,
                    "blink_max_count": False,
                    "max_saccade_dur": False,
                    "fixation_min_cutoff": 10,
                }
            ),
        )
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [Fixation(Point(0, 0), 0, 25, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should("not include fixations before the start of a trial.")
    def test_fix_before_synctime():
        fixations = """
        MSG 1000 TRIALID E1I1D0
        MSG 1001 REGION CHAR 1 1 T 10 100 20 110
        MSG 1002 REGION CHAR 1 1 e 20 100 30 110
        MSG 1003 REGION CHAR 1 1 s 30 100 40 110
        MSG 1004 REGION CHAR 1 1 t 40 100 50 110
        MSG 1005 REGION CHAR 1 1   50 100 60 110
        MSG 1006 REGION CHAR 1 1 i 60 100 70 110
        MSG 1007 REGION CHAR 1 1 t 70 100 80 110
        MSG 1008 REGION CHAR 1 1 e 80 100 90 110
        MSG 1009 REGION CHAR 1 1 m 90 100 100 110
        EFIX R 2000 2005 5 12 105 0
        MSG 2001 SYNCTIME
        EFIX R 2005 2020 15 33 105 0
        """
        parsed_experiment = parser.asc.get_trials(
            fixations + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": False,
                    "blink_max_count": False,
                    "max_saccade_dur": False,
                    "fixation_min_cutoff": 10,
                }
            ),
        )
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                8000,
                it.items["1"]["1"],
                [Fixation(Point(2, 0), 0, 15, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should(
        "merge a previous fixation shorter than fixation_min_cutoff with the next fixation"
    )
    def test_first_fix_merge():
        fixations = "EFIX R 2000 2005 5 12 105 0\nEFIX R 2005 2020 15 33 105 0"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixations + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": False,
                    "blink_max_count": False,
                    "max_saccade_dur": False,
                    "fixation_min_cutoff": 10,
                }
            ),
        )
        it.assertEqual(
            parsed_experiment[0],
            Trial(
                0,
                10000,
                it.items["1"]["1"],
                [Fixation(Point(2, 0), 0, 20, 0, it.items["1"]["1"].regions[0])],
            ),
        )

    @it.should("exclude trials with saccade duration longer than max_saccade_dur")
    def test_exclude_saccade_trial():
        fixations = "EFIX R 2000 2005 5 12 105 0\nEFIX R 2025 2030 5 33 105 0"
        parsed_experiment = parser.asc.get_trials(
            it.asc_header + fixations + it.asc_end,
            it.items,
            config.ASCParsingConfig(
                {
                    "blink_max_dur": False,
                    "blink_max_count": False,
                    "max_saccade_dur": 10,
                    "fixation_min_cutoff": False,
                }
            ),
        )
        it.assertEqual(parsed_experiment, [])

    with it.having("get_lines") as it:

        @it.should("cluster character coordinates into lines")
        def test_get_lines():
            chars = [
                {"char": "a", "x1": 0, "x2": 10, "y1": 10, "y2": 20},
                {"char": "b", "x1": 10, "x2": 20, "y1": 9, "y2": 20},
                {"char": "c", "x1": 20, "x2": 30, "y1": 11, "y2": 23},
                {"char": "d", "x1": 0, "x2": 10, "y1": 30, "y2": 40},
                {"char": "e", "x1": 10, "x2": 20, "y1": 29, "y2": 41},
                {"char": "f", "x1": 0, "x2": 10, "y1": 50, "y2": 60},
                {"char": "g", "x1": 10, "x2": 20, "y1": 54, "y2": 63},
            ]
            expected_chars = [
                {
                    "char": "a",
                    "x1": 0,
                    "x2": 10,
                    "y1": 10,
                    "y2": 20,
                    "line_pos": 0,
                    "char_pos": 0,
                },
                {
                    "char": "b",
                    "x1": 10,
                    "x2": 20,
                    "y1": 9,
                    "y2": 20,
                    "line_pos": 0,
                    "char_pos": 1,
                },
                {
                    "char": "c",
                    "x1": 20,
                    "x2": 30,
                    "y1": 11,
                    "y2": 23,
                    "line_pos": 0,
                    "char_pos": 2,
                },
                {
                    "char": "d",
                    "x1": 0,
                    "x2": 10,
                    "y1": 30,
                    "y2": 40,
                    "line_pos": 1,
                    "char_pos": 0,
                },
                {
                    "char": "e",
                    "x1": 10,
                    "x2": 20,
                    "y1": 29,
                    "y2": 41,
                    "line_pos": 1,
                    "char_pos": 1,
                },
                {
                    "char": "f",
                    "x1": 0,
                    "x2": 10,
                    "y1": 50,
                    "y2": 60,
                    "line_pos": 2,
                    "char_pos": 0,
                },
                {
                    "char": "g",
                    "x1": 10,
                    "x2": 20,
                    "y1": 54,
                    "y2": 63,
                    "line_pos": 2,
                    "char_pos": 1,
                },
            ]
            it.assertEqual(parser.asc.get_lines(chars), expected_chars)


it.createTests(globals())
