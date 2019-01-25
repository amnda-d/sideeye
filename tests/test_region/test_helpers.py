from nose2.tools import such
from sideeye.measures.helpers import get_fp_fixations
from sideeye.data import Point, Fixation, Region, Item, Trial

with such.A('Region Measure Helpers') as it:
    @it.has_setup
    def setup():
        it.regions_x = [
            Region(Point(0, 0), Point(10, 0)),
            Region(Point(10, 0), Point(20, 0)),
            Region(Point(20, 0), Point(30, 0)),
            Region(Point(30, 0), Point(40, 0))]
        it.item_x = Item(1, 1, it.regions_x)
        it.fixations_x = [
            Fixation(Point(0, 0), 0, 100, 0, it.regions_x[0]),
            Fixation(Point(3, 0), 100, 200, 1, it.regions_x[0]),
            Fixation(Point(22, 0), 200, 300, 2, it.regions_x[2]),
            Fixation(Point(12, 0), 300, 400, 3, it.regions_x[1])
        ]
        it.trial_x = Trial(1, 400, it.item_x, it.fixations_x)

        it.excluded_fix = [
            Fixation(Point(1, 0), 0, 50, 0, it.regions_x[0], excluded=True),
            Fixation(Point(2, 0), 50, 100, 1, it.regions_x[0], excluded=False),
            Fixation(Point(22, 0), 110, 150, 2, it.regions_x[2], excluded=True),
            Fixation(Point(13, 0), 200, 250, 3, it.regions_x[1], excluded=False),
            Fixation(Point(1, 0), 300, 350, 4, it.regions_x[0], excluded=True)
        ]

        it.excluded_trial = Trial(1, 350, it.item_x, it.excluded_fix)

        it.regions_y = [
            Region(Point(0, 0), Point(10, 0)),
            Region(Point(10, 0), Point(0, 1)),
            Region(Point(0, 1), Point(10, 1)),
            Region(Point(10, 1), Point(20, 1))
        ]
        it.item_y = Item(2, 1, it.regions_y)
        it.fixations_y = [
            Fixation(Point(12, 0), 0, 100, 0, it.regions_y[1]),
            Fixation(Point(12, 1), 100, 200, 1, it.regions_y[3]),
            Fixation(Point(15, 1), 200, 300, 2, it.regions_y[3]),
            Fixation(Point(8, 0), 300, 400, 3, it.regions_y[0])
        ]
        it.trial_y = Trial(1, 400, it.item_y, it.fixations_y)

        it.fixations_x2 = [
            Fixation(Point(0, 0), 0, 150, 0, it.regions_x[0]),
            Fixation(Point(3, 0), 150, 200, 1, it.regions_x[0]),
            Fixation(Point(14, 0), 200, 350, 2, it.regions_x[1]),
            Fixation(Point(12, 0), 350, 400, 3, it.regions_x[1]),
            Fixation(Point(3, 0), 400, 550, 4, it.regions_x[0]),
            Fixation(Point(11, 0), 650, 700, 5, it.regions_x[1]),
            Fixation(Point(21, 0), 750, 800, 6, it.regions_x[2]),
            Fixation(Point(11, 0), 850, 900, 7, it.regions_x[1])
        ]
        it.trial_x2 = Trial(1, 600, it.item_x, it.fixations_x2)

    with it.having('first pass fixations'):
        @it.should('return a list of first pass fixations')
        def test_fp_fixations():
            it.assertEqual(
                get_fp_fixations(it.trial_x, 0),
                [it.fixations_x[0], it.fixations_x[1]]
            )
            it.assertEqual(
                get_fp_fixations(it.trial_y, 3),
                [it.fixations_y[1], it.fixations_y[2]]
            )
            it.assertEqual(
                get_fp_fixations(it.trial_x2, 1),
                [it.fixations_x2[2], it.fixations_x2[3]]
            )
            it.assertEqual(
                get_fp_fixations(it.trial_x, 2),
                [it.fixations_x[2]]
            )

        @it.should('not include excluded fixations')
        def test_fp_excluded():
            it.assertEqual(get_fp_fixations(it.excluded_trial, 0), [it.excluded_fix[1]])

        @it.should('return an empty list if there are no first pass fixations')
        def test_no_fp_fixations():
            it.assertEqual(get_fp_fixations(it.trial_x, 1), [])
            it.assertEqual(get_fp_fixations(it.trial_x, 3), [])
            it.assertEqual(get_fp_fixations(it.trial_y, 0), [])
            it.assertEqual(get_fp_fixations(it.trial_y, 2), [])

it.createTests(globals())
