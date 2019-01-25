from nose2.tools import such
from sideeye import measures
from sideeye.data import Point, Fixation, Region, Item, Trial

with such.A('Other Region Measures') as it:
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
            Fixation(Point(22, 0), 300, 300, 3, it.regions_x[2], excluded=True),
            Fixation(Point(12, 0), 300, 400, 4, it.regions_x[1])
        ]
        it.trial_x = Trial(1, 400, it.item_x, it.fixations_x)

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
            Fixation(Point(12, 1), 200, 200, 2, it.regions_y[3], excluded=True),
            Fixation(Point(15, 1), 200, 300, 3, it.regions_y[3]),
            Fixation(Point(8, 0), 300, 400, 4, it.regions_y[0])
        ]
        it.trial_y = Trial(1, 400, it.item_y, it.fixations_y)

    with it.having('landing position measure'):
        @it.should('calculate landing position correctly')
        def test_landing_position():
            it.assertEqual(measures.region.landing_position(it.trial_x, 2)['value'], '"(2, 0)"')
            it.assertEqual(measures.region.landing_position(it.trial_y, 1)['value'], '"(2, 0)"')
            it.assertEqual(measures.region.landing_position(it.trial_x, 0)['value'], '"(0, 0)"')
            it.assertEqual(measures.region.landing_position(it.trial_y, 3)['value'], '"(2, 0)"')

        @it.should('be None if the region is skipped')
        def test_landing_position_skip():
            it.assertEqual(measures.region.landing_position(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.landing_position(it.trial_y, 2)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_landing_position_error():
            with it.assertRaises(ValueError):
                measures.region.landing_position(it.trial_x, 5)

    with it.having('launch site measure'):
        @it.should('calculate launch site correctly')
        def test_launch_site():
            it.assertEqual(measures.region.launch_site(it.trial_x, 2)['value'], '"(-17, 0)"')
            it.assertEqual(measures.region.launch_site(it.trial_y, 3)['value'], '"(2, -1)"')

        @it.should('be None if the region is skipped or there is no prior fixation')
        def test_launch_site_skip():
            it.assertEqual(measures.region.launch_site(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.launch_site(it.trial_y, 2)['value'], None)
            it.assertEqual(measures.region.launch_site(it.trial_x, 0)['value'], None)
            it.assertEqual(measures.region.launch_site(it.trial_y, 1)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_launch_site_error():
            with it.assertRaises(ValueError):
                measures.region.launch_site(it.trial_x, 5)

    with it.having('first pass fixation count measure'):
        @it.should('calculate first pass fixation count correctly')
        def test_fixation_count():
            it.assertEqual(measures.region.first_pass_fixation_count(it.trial_x, 2)['value'], 1)
            it.assertEqual(measures.region.first_pass_fixation_count(it.trial_y, 1)['value'], 1)
            it.assertEqual(measures.region.first_pass_fixation_count(it.trial_x, 0)['value'], 2)
            it.assertEqual(measures.region.first_pass_fixation_count(it.trial_y, 3)['value'], 2)

        @it.should('be None if the region is skipped')
        def test_fixation_count_skip():
            it.assertEqual(measures.region.first_pass_fixation_count(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.first_pass_fixation_count(it.trial_y, 2)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_fixation_count_error():
            with it.assertRaises(ValueError):
                measures.region.first_pass_fixation_count(it.trial_x, 5)


it.createTests(globals())
