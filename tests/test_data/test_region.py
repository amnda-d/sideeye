from nose2.tools import such
from sideeye import Point, Region

with such.A('Region') as it:
    @it.should('only allow valid regions')
    def test_region_validation():
        with it.assertRaises(ValueError):
            Region(Point(0, 1), Point(10, 0), 1, 'invalid: y2 < y1')
        with it.assertRaises(ValueError):
            Region(Point(10, 1), Point(7, 1), 1, 'invalid: x2 < x1')
        with it.assertRaises(ValueError):
            Region(Point(-1, 0), Point(1, 1), 1, 'invalid: negative position')
        with it.assertRaises(ValueError):
            Region(Point(-1, 0), Point(1, 1), -1, 'invalid: negative position')

    @it.should('have equality defined correctly')
    def test_region_equality():
        it.assertTrue(
            Region(Point(0, 1), Point(10, 1), 1, 'r') == Region(Point(0, 1), Point(10, 1), 1, 'r')
        )
        it.assertTrue(
            Region(Point(0, 1), Point(10, 1), 1, 'r') != Region(Point(0, 1), Point(10, 2), 1, 'r')
        )

it.createTests(globals())
