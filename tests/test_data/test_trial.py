from nose2.tools import such
from sideeye import Point, Fixation, Saccade, Region, Item, Trial

with such.A('Trial') as it:
    @it.has_setup
    def setup():
        it.r1 = Region(Point(1, 1), Point(2, 2), 1, 'region 1')
        it.r2 = Region(Point(1, 1), Point(2, 2), 1, 'region 2')
        it.r3 = Region(Point(1, 1), Point(2, 2), 1, 'region 3')
        it.fix1 = Fixation(Point(1, 2), 3, 4, 0, 'region')
        it.fix2 = Fixation(Point(1, 2), 5, 6, 1, 'region')
        it.fixations = [
            Fixation(Point(1, 2), 10, 20, 0, 'region'),
            Fixation(Point(1, 2), 30, 40, 1, 'region'),
            Fixation(Point(1, 2), 50, 60, 2, 'region'),
            Fixation(Point(1, 2), 70, 80, 3, 'region', excluded=True),
            Fixation(Point(1, 2), 90, 100, 4, 'region'),
            Fixation(Point(1, 2), 110, 120, 5, 'region', excluded=True),
            Fixation(Point(1, 2), 130, 140, 6, 'region', excluded=True),
            Fixation(Point(1, 2), 150, 160, 7, 'region'),
            Fixation(Point(1, 2), 170, 180, 8, 'region', excluded=True)
        ]
        it.item = Item(2, 1, [it.r1, it.r2, it.r3])
        it.trial = Trial(1, 5, it.item, it.fixations)
        it.trial_include_fixations = Trial(1, 5, it.item, it.fixations, include_fixation=True)
        it.trial_include_saccades = Trial(1, 5, it.item, it.fixations, include_saccades=True)
        it.trial_include_both = Trial(
            1, 5, it.item, it.fixations, include_fixation=True, include_saccades=True
        )

    @it.should('return the correct number of fixations')
    def test_fixations_count():
        it.assertEqual(it.trial.fixation_count(), 5)

    @it.should('calculate saccades correctly')
    def test_saccades():
        saccades = [
            Saccade(10, False, it.fixations[0], it.fixations[1]),
            Saccade(10, False, it.fixations[1], it.fixations[2])
        ]
        it.assertEqual(it.trial.saccades, saccades)

    @it.should('calculate saccades correctly when include_fixation=True')
    def test_include_fixation():
        saccades = [
            Saccade(10, False, it.fixations[0], it.fixations[1]),
            Saccade(10, False, it.fixations[1], it.fixations[2]),
            Saccade(10, False, it.fixations[2], it.fixations[4]),
            Saccade(20, False, it.fixations[4], it.fixations[7]),
        ]
        it.assertEqual(it.trial_include_fixations.saccades, saccades)

    @it.should('calculate saccades correctly when include_saccades=True')
    def test_include_saccade():
        saccades = [
            Saccade(10, False, it.fixations[0], it.fixations[1]),
            Saccade(10, False, it.fixations[1], it.fixations[2]),
            Saccade(20, False, it.fixations[2], it.fixations[4]),
            Saccade(30, False, it.fixations[4], it.fixations[7]),
        ]
        it.assertEqual(it.trial_include_saccades.saccades, saccades)

    @it.should('calculate saccades correctly when include_saccades and include_fixation are True')
    def test_include_saccade_fixation():
        saccades = [
            Saccade(10, False, it.fixations[0], it.fixations[1]),
            Saccade(10, False, it.fixations[1], it.fixations[2]),
            Saccade(30, False, it.fixations[2], it.fixations[4]),
            Saccade(50, False, it.fixations[4], it.fixations[7]),
        ]
        it.assertEqual(it.trial_include_both.saccades, saccades)

    @it.should('not allow trials with index < 0')
    def test_trial_index():
        with it.assertRaises(ValueError):
            Trial(-1, 5, it.item, it.fixations)

    @it.should('not allow trials without an Item')
    def test_trial_validation():
        with it.assertRaises(ValueError):
            Trial(1, 5, None, it.fixations)

    @it.should('have equality defined correctly')
    def test_trial_equality():
        it.assertTrue(Trial(1, 5, it.item, it.fixations) == Trial(1, 5, it.item, it.fixations))
        it.assertTrue(
            Trial(1, 5, it.item, it.fixations) != Trial(1, 5, it.item, [it.fix1, it.fix2])
        )

it.createTests(globals())
