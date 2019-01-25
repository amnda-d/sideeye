from nose2.tools import such
from sideeye import Point, Fixation

with such.A('Fixation') as it:
    @it.has_test_setup
    def setup():
        it.fix1 = Fixation(Point(1, 2), 3, 4, 0, 'region')
        it.fix2 = Fixation(Point(1, 2), 3, 4, 1, 'region')
        it.fix3 = Fixation(Point(1, 3), 3, 4, 2, 'region')
        it.fix1.region = 'region'

    @it.should('calculate duration correctly')
    def test_duration():
        it.assertEqual(it.fix1.duration, 1)

    @it.should('have an assigned region')
    def test_region():
        it.assertEqual(it.fix1.region, 'region')

    @it.should('have equality defined correctly')
    def test_fixation_equality():
        it.assertTrue(
            Fixation(Point(1, 2), 3, 4, 0, 'region') == Fixation(Point(1, 2), 3, 4, 0, 'region')
        )
        it.assertTrue(
            Fixation(Point(1, 2), 3, 4, 1, 'region') != Fixation(Point(1, 3), 3, 4, 1, 'region')
        )

    @it.should('only allow valid fixations')
    def test_fixation_validation():
        with it.assertRaises(ValueError):
            Fixation(Point(1, 2), 5, 1, 0, 'region')

    @it.should('exclude fixations with negative position')
    def test_negative_fixation():
        it.assertEqual(Fixation(Point(-1, 0), 1, 2, 0, 'region').excluded, True)

it.createTests(globals())
