from nose2.tools import such
from sideeye import Point, Fixation, Saccade

with such.A('Saccade') as it:
    @it.has_test_setup
    def setup():
        it.fix1 = Fixation(Point(1, 2), 3, 4, 0, 'region')
        it.fix2 = Fixation(Point(1, 2), 5, 6, 1, 'region')

    @it.should('only allow valid saccades')
    def test_saccade_validation():
        with it.assertRaises(ValueError):
            Saccade(-10, False, it.fix1, it.fix2)
        with it.assertRaises(ValueError):
            Saccade(-100, True, it.fix1, it.fix2)

    @it.should('have equality defined correctly')
    def test_saccade_equality():
        it.assertTrue(Saccade(10, True, it.fix1, it.fix2) == Saccade(10, True, it.fix1, it.fix2))
        it.assertTrue(Saccade(10, False, it.fix1, it.fix2) != Saccade(50, False, it.fix1, it.fix2))
        it.assertTrue(Saccade(10, False, it.fix1, it.fix2) != Saccade(10, True, it.fix1, it.fix2))

it.createTests(globals())
