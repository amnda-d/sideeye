import os

from sideeye import parser, Point, Fixation, Trial, Region, Item

from nose2.tools import such

class TestData(object):

    @classmethod
    def setUp(cls):
        it.testdata = True

    @classmethod
    def tearDown(cls):
        del it.testdata

with such.A('Region String Parser') as it:
    with it.having('single item region string parser'):
        @it.has_setup
        def setup():
            it.region = parser.region.text('This is/ a string/ with four/ regions')
            it.parsed_regions = [Region(Point(0, 0), Point(7, 0), 7, 'This is'),
                                 Region(Point(7, 0), Point(16, 0), 9, ' a string'),
                                 Region(Point(16, 0), Point(26, 0), 10, ' with four'),
                                 Region(Point(26, 0), Point(34, 0), 8, ' regions')]

        @it.should('parse a region string')
        def test_region_string():
            it.assertEqual(it.region, it.parsed_regions)

        @it.should('throw an error when given a non-region string input')
        def test_non_region_string():
            with it.assertRaises(ValueError):
                parser.region.text(1)

    with it.having('text file region string parser'):
        @it.has_setup
        def setup():
            it.dirname = os.path.dirname(os.path.realpath(__file__))
            it.txt_items = parser.region.textfile(os.path.join(it.dirname, 'testdata/regionstring.txt'))

        @it.should('parse a region string text file')
        def test_region_string_file():
            it.assertEqual(it.txt_items[1][1],
                           Item(1, 1, [Region(Point(0, 0), Point(17, 0), 17, 'this is region 1 '),
                                       Region(Point(17, 0), Point(33, 0), 16, 'this is region 2'),
                                       Region(Point(33, 0), Point(50, 0), 17, ' this is region 3'),
                                       Region(Point(50, 0), Point(18, 1), 18, 'this is a new line'),
                                       Region(Point(18, 1), Point(40, 1), 22, 'this is another region'),
                                       Region(Point(40, 1), Point(20, 2), 20, 'this is a third line')]))
            it.assertEqual(it.txt_items[1][2],
                           Item(1, 2, [Region(Point(0, 0), Point(20, 0), 20, 'item with one region')]))
            it.assertEqual(it.txt_items[2][1],
                           Item(2, 1, [Region(Point(0, 0), Point(9, 0), 9, 'item with'),
                                       Region(Point(9, 0), Point(19, 1), 19, 'one region per line')]))
            it.assertEqual(it.txt_items[2][2],
                           Item(2, 2, [Region(Point(0, 0), Point(8, 0), 8, 'this is '),
                                       Region(Point(8, 0), Point(16, 0), 8, 'an item '),
                                       Region(Point(16, 0), Point(20, 0), 4, 'with'),
                                       Region(Point(20, 0), Point(12, 1), 12, 'three lines '),
                                       Region(Point(12, 1), Point(22, 1), 10, 'of regions'),
                                       Region(Point(22, 1), Point(21, 2), 21, 'and multiple regions '),
                                       Region(Point(21, 2), Point(29, 2), 8, 'per line')]))
            it.assertEqual(it.txt_items[3][1],
                           Item(3, 1, [Region(Point(0, 0), Point(10, 1), 20, 'this is an\nitem with '),
                                       Region(Point(10, 1), Point(46, 1), 36, 'a new line in the middle of a region')]))


it.createTests(globals())
