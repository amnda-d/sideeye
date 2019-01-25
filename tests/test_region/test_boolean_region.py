from nose2.tools import such
from sideeye import measures
from sideeye.data import Point, Fixation, Region, Item, Trial

with such.A('Boolean Region Measures') as it:
    @it.has_setup
    def setup():
        # /aaaaaaaaaa/aaaaaaaaaa/aaaaaaaaaa/aaaaaaaaaa/
        it.regions_x = [
            Region(Point(0, 0), Point(10, 0)),
            Region(Point(10, 0), Point(20, 0)),
            Region(Point(20, 0), Point(30, 0)),
            Region(Point(30, 0), Point(40, 0))
        ]
        it.item_x = Item(1, 1, it.regions_x)
        it.fixations_x = [
            Fixation(Point(0, 0), 0, 100, 0, it.regions_x[0]),
            Fixation(Point(3, 0), 100, 200, 1, it.regions_x[0]),
            Fixation(Point(22, 0), 200, 300, 2, it.regions_x[2]),
            Fixation(Point(12, 0), 300, 400, 3, it.regions_x[1])
        ]
        it.trial_x = Trial(1, 400, it.item_x, it.fixations_x)

        it.excluded_fix = [
            Fixation(Point(1, 0), 0, 100, 4, it.regions_x[0], excluded=False),
            Fixation(Point(22, 0), 110, 150, 5, it.regions_x[2], excluded=True),
            Fixation(Point(13, 0), 200, 250, 6, it.regions_x[1], excluded=False),
            Fixation(Point(1, 0), 300, 350, 7, it.regions_x[0], excluded=True)
        ]

        it.excluded_trial = Trial(1, 350, it.item_x, it.excluded_fix)

        # aaaaaaaaaa/aaaaaaaaa.../
        # aaaaaaaaaa/aaaaaaaaaa/
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

    with it.having('skip measure'):
        @it.should('''be true if there is a fixation in a future region before
                      there is a fixation in the target region''')
        def test_skip_fixation():
            it.assertTrue(measures.region.skip(it.trial_x, 1)['value'])
            it.assertTrue(measures.region.skip(it.trial_y, 0)['value'])

        @it.should('be true if there is never a fixation in the target region')
        def test_skip_no_fixation():
            it.assertTrue(measures.region.skip(it.trial_x, 3)['value'])
            it.assertTrue(measures.region.skip(it.trial_y, 2)['value'])

        @it.should('be false if the region is not skipped')
        def test_skip_false():
            it.assertFalse(measures.region.skip(it.trial_x, 2)['value'])
            it.assertFalse(measures.region.skip(it.trial_y, 1)['value'])

        @it.should('throw an error if the target region does not exist in the trial')
        def test_skip_error():
            with it.assertRaises(ValueError):
                measures.region.skip(it.trial_x, 5)

        @it.should('not included excluded fixations')
        def test_skip_excluded():
            it.assertTrue(measures.region.skip(it.excluded_trial, 2)['value'])

    with it.having('first pass regressions out measure'):
        @it.should('be true if there is a regression out of the target region')
        def test_regressions_out_true():
            it.assertTrue(measures.region.first_pass_regressions_out(it.trial_x, 2)['value'])
            it.assertTrue(measures.region.first_pass_regressions_out(it.trial_y, 3)['value'])

        @it.should('be false if there is not a regression out of the target region')
        def test_regressions_out_false():
            it.assertFalse(measures.region.first_pass_regressions_out(it.trial_x, 0)['value'])
            it.assertFalse(measures.region.first_pass_regressions_out(it.trial_y, 1)['value'])

        @it.should('be None if the region is never fixated')
        def test_regressions_out_none():
            it.assertEqual(measures.region.first_pass_regressions_out(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.first_pass_regressions_out(it.trial_y, 2)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_regressions_out_error():
            with it.assertRaises(ValueError):
                measures.region.first_pass_regressions_out(it.trial_y, 6)

        @it.should('not include excluded fixations')
        def test_regressions_out_exclude():
            it.assertFalse(
                measures.region.first_pass_regressions_out(it.excluded_trial, 1)['value']
            )

    with it.having('first pass regressions in measure'):
        @it.should('be true if there is a regression into the target region')
        def test_regressions_in_true():
            it.assertTrue(measures.region.first_pass_regressions_in(it.trial_x, 1)['value'])
            it.assertTrue(measures.region.first_pass_regressions_in(it.trial_y, 0)['value'])

        @it.should('be false if there is not a regression into the target region')
        def test_regressions_in_false():
            it.assertFalse(measures.region.first_pass_regressions_in(it.trial_x, 2)['value'])
            it.assertFalse(measures.region.first_pass_regressions_in(it.trial_y, 3)['value'])

        @it.should('be None if the region is never fixated')
        def test_regressions_in_none():
            it.assertEqual(measures.region.first_pass_regressions_in(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.first_pass_regressions_in(it.trial_y, 2)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_regressions_in_error():
            with it.assertRaises(ValueError):
                measures.region.first_pass_regressions_in(it.trial_y, 6)

        @it.should('not include excluded fixations')
        def test_regressions_in_exclude():
            it.assertFalse(measures.region.first_pass_regressions_in(it.excluded_trial, 0)['value'])


it.createTests(globals())
