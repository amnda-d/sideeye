import os
from nose2.tools import such
from sideeye import config, parser, Point, Fixation, Trial, Region, Item

with such.A("Parser") as it:
    with it.having("DA1 parser"):

        @it.has_setup
        def setup_da1():
            it.dirname = os.path.dirname(os.path.realpath(__file__))
            it.timdrop_items = parser.region.file(
                os.path.join(it.dirname, "testdata/timdropDA1.cnt")
            )
            it.config = config.Configuration()
            it.config.region_fields.number = 1
            it.config.region_fields.condition = 0
            it.config.region_fields.boundaries_start = 3
            it.config.region_fields.includes_y = True
            it.robodoc_items = parser.region.file(
                os.path.join(it.dirname, "testdata/robodocDA1.reg"), it.config
            )
            it.timdrop_DA1 = parser.da1.parse(
                os.path.join(it.dirname, "testdata/timdrop.DA1"),
                it.timdrop_items,
                it.config,
            )
            it.config.da1_fields.time = 3
            it.robodoc_DA1 = parser.da1.parse(
                os.path.join(it.dirname, "testdata/robodoc.DA1"),
                it.robodoc_items,
                it.config,
            )

        @it.should("parse a timdrop DA1 file")
        def test_da1():
            it.timdrop_fixations = [
                Fixation(
                    Point(-1, -1),
                    0,
                    170,
                    0,
                    Region(Point(0, 0), Point(20, 0), label=0, number=0),
                ),
                Fixation(
                    Point(7, 0),
                    195,
                    587,
                    1,
                    Region(Point(0, 0), Point(20, 0), label=0, number=0),
                ),
                Fixation(
                    Point(24, 0),
                    627,
                    841,
                    2,
                    Region(Point(20, 0), Point(26, 0), label=1, number=1),
                ),
                Fixation(
                    Point(46, 0),
                    892,
                    1157,
                    3,
                    Region(Point(38, 0), Point(75, 0), label=4, number=4),
                ),
                Fixation(
                    Point(58, 0),
                    1184,
                    1424,
                    4,
                    Region(Point(38, 0), Point(75, 0), label=4, number=4),
                ),
                Fixation(
                    Point(70, 0),
                    1452,
                    1779,
                    5,
                    Region(Point(38, 0), Point(75, 0), label=4, number=4),
                ),
            ]
            it.trial1 = Trial(
                1, 1779, it.timdrop_items["286"]["2"], it.timdrop_fixations
            )
            it.assertEqual(it.timdrop_DA1.trials[("286", "2")], it.trial1)

        @it.should("parse a robodoc DA1 file")
        def test_da1_robodoc():
            it.robodoc_fixations = [
                Fixation(
                    Point(6, 0),
                    1241,
                    1410,
                    0,
                    Region(Point(0, 0), Point(17, 0), label=0, number=0),
                ),
                Fixation(
                    Point(4, 0),
                    1429,
                    1796,
                    1,
                    Region(Point(0, 0), Point(17, 0), label=0, number=0),
                ),
                Fixation(
                    Point(16, 0),
                    1822,
                    2223,
                    2,
                    Region(Point(0, 0), Point(17, 0), label=0, number=0),
                ),
                Fixation(
                    Point(6, 0),
                    2245,
                    2471,
                    3,
                    Region(Point(0, 0), Point(17, 0), label=0, number=0),
                ),
                Fixation(
                    Point(24, 0),
                    2504,
                    3232,
                    4,
                    Region(Point(17, 0), Point(29, 0), label=1, number=1),
                ),
                Fixation(
                    Point(32, 0),
                    3262,
                    3520,
                    5,
                    Region(Point(29, 0), Point(40, 0), label=2, number=2),
                ),
                Fixation(
                    Point(39, 0),
                    3552,
                    3894,
                    6,
                    Region(Point(29, 0), Point(40, 0), label=2, number=2),
                ),
                Fixation(
                    Point(44, 0),
                    3924,
                    4164,
                    7,
                    Region(Point(40, 0), Point(52, 0), label=3, number=3),
                ),
                Fixation(
                    Point(55, 0),
                    4189,
                    4671,
                    8,
                    Region(Point(52, 0), Point(65, 0), label=4, number=4),
                ),
                Fixation(
                    Point(49, 0),
                    4696,
                    4931,
                    9,
                    Region(Point(40, 0), Point(52, 0), label=3, number=3),
                ),
                Fixation(
                    Point(69, 0),
                    4959,
                    5250,
                    10,
                    Region(Point(65, 0), Point(77, 0), label=5, number=5),
                ),
                Fixation(
                    Point(65, 0),
                    5271,
                    5633,
                    11,
                    Region(Point(65, 0), Point(77, 0), label=5, number=5),
                ),
                Fixation(
                    Point(72, 0),
                    5656,
                    5885,
                    12,
                    Region(Point(65, 0), Point(77, 0), label=5, number=5),
                ),
                Fixation(
                    Point(81, 0),
                    5910,
                    6278,
                    13,
                    Region(Point(77, 0), Point(95, 0), label=6, number=6),
                ),
                Fixation(
                    Point(87, 0),
                    6300,
                    6625,
                    14,
                    Region(Point(77, 0), Point(95, 0), label=6, number=6),
                ),
                Fixation(
                    Point(81, 0),
                    6647,
                    6851,
                    15,
                    Region(Point(77, 0), Point(95, 0), label=6, number=6),
                ),
                Fixation(
                    Point(78, 0),
                    6873,
                    7231,
                    16,
                    Region(Point(77, 0), Point(95, 0), label=6, number=6),
                ),
                Fixation(
                    Point(87, 0),
                    7256,
                    7768,
                    17,
                    Region(Point(77, 0), Point(95, 0), label=6, number=6),
                ),
            ]
            it.trial7 = Trial(
                7, 7792, it.robodoc_items["58"]["12"], it.robodoc_fixations
            )
            it.assertEqual(it.robodoc_DA1.trials[("58", "12")], it.trial7)

        @it.should("throw an error when given a non-DA1 file input")
        def test_non_da1():
            with it.assertRaises(ValueError):
                parser.da1.parse(
                    os.path.join(it.dirname, "testdata/robodocDA1.reg"),
                    it.robodoc_items,
                )
            with it.assertRaises(ValueError):
                parser.da1.parse(
                    os.path.join(it.dirname, "testdata/timdrop.DA1"),
                    it.robodoc_items,
                    da1_type="robodoc",
                )

    with it.having("region parser"):

        @it.has_setup
        def setup_region():
            it.dirname = os.path.dirname(os.path.realpath(__file__))
            it.config = config.Configuration()
            it.config.region_fields.number = 1
            it.config.region_fields.condition = 0
            it.config.region_fields.boundaries_start = 3
            it.config.region_fields.includes_y = True
            it.reg = parser.region.file(
                os.path.join(it.dirname, "testdata/robodocDA1.reg"), it.config
            )
            it.config.region_fields.number = 0
            it.config.region_fields.condition = 1
            it.config.region_fields.boundaries_start = 3
            it.config.region_fields.includes_y = False
            it.cnt = parser.region.file(
                os.path.join(it.dirname, "testdata/timdropDA1.cnt"), it.config
            )
            it.reg_regions = [
                Region(Point(0, 0), Point(11, 0)),
                Region(Point(11, 0), Point(21, 0)),
                Region(Point(21, 0), Point(34, 0)),
                Region(Point(34, 0), Point(45, 0)),
                Region(Point(45, 0), Point(61, 0)),
                Region(Point(61, 0), Point(73, 0)),
                Region(Point(73, 0), Point(92, 0)),
            ]
            it.reg_item = Item("57", "11", it.reg_regions)
            it.cnt_regions = [
                Region(Point(0, 0), Point(15, 0)),
                Region(Point(15, 0), Point(19, 0)),
                Region(Point(19, 0), Point(25, 0)),
                Region(Point(25, 0), Point(28, 0)),
                Region(Point(28, 0), Point(47, 0)),
            ]
            it.cnt_item = Item("1", "1", it.cnt_regions)

        @it.should("parse a reg file")
        def test_reg():
            it.assertEqual(it.reg["57"]["11"], it.reg_item)

        @it.should("parse a cnt file")
        def test_cnt():
            it.assertEqual(it.cnt["1"]["1"], it.cnt_item)

        @it.should("throw an error when given a non-region file input")
        def test_non_reg():
            with it.assertRaises(ValueError):
                it.config.region_fields.number = 1
                it.config.region_fields.condition = 0
                it.config.region_fields.boundaries_start = 3
                it.config.region_fields.includes_y = False
                parser.region.file(
                    os.path.join(it.dirname, "testdata/robodoc.DA1"), it.config
                )


it.createTests(globals())
