from nose2.tools import such
from sideeye import measures
from sideeye.data import Point, Fixation, Region, Item, Trial

with such.A('Trial Measures') as it:
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
            Fixation(Point(0, 0), 0, 100, it.regions_x[0]),
            Fixation(Point(3, 0), 120, 200, it.regions_x[0]),
            Fixation(Point(22, 0), 230, 300, it.regions_x[2]),
            Fixation(Point(12, 0), 340, 400, it.regions_x[1]),
            Fixation(Point(15, 0), 400, 450, it.regions_x[1], excluded=True)
        ]
        it.trial_x = Trial(1, 400, it.item_x, it.fixations_x)

        it.no_regressions_fix = [
            Fixation(Point(0, 0), 0, 100, it.regions_x[0]),
            Fixation(Point(3, 0), 110, 200, it.regions_x[0]),
            Fixation(Point(22, 0), 220, 300, it.regions_x[2]),
            Fixation(Point(31, 0), 330, 400, it.regions_x[3])
        ]

        it.no_regressions = Trial(1, 400, it.item_x, it.no_regressions_fix)

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
            Fixation(Point(12, 0), 0, 100, it.regions_y[1]),
            Fixation(Point(12, 1), 110, 200, it.regions_y[3]),
            Fixation(Point(15, 1), 220, 300, it.regions_y[3]),
            Fixation(Point(8, 0), 330, 400, it.regions_y[0])
        ]
        it.trial_y = Trial(1, 400, it.item_y, it.fixations_y)

    with it.having('location of first regression measure'):
        @it.should('''return the correct position of the last fixation before the
                      first regression in a trial.''')
        def test_location_first_regression():
            it.assertEqual(measures.trial.location_first_regression(it.trial_x), '"(22, 0)"')
            it.assertEqual(measures.trial.location_first_regression(it.trial_y), '"(15, 1)"')
            it.assertEqual(measures.trial.location_first_regression(it.no_regressions), None)

    with it.having('latency to first regression measure'):
        @it.should('''return the correct time until the end of the last fixation
                      before the first regression in a trial.''')
        def test_latency_first_regression():
            it.assertEqual(measures.trial.latency_first_regression(it.trial_x), 300)
            it.assertEqual(measures.trial.latency_first_regression(it.trial_y), 300)
            it.assertEqual(measures.trial.latency_first_regression(it.no_regressions), None)

    with it.having('fixation count measure'):
        @it.should('return the correct number of fixations in a trial')
        def test_fixation_count():
            it.assertEqual(measures.trial.fixation_count(it.trial_x), 4)
            it.assertEqual(measures.trial.fixation_count(it.trial_y), 4)
            it.assertEqual(measures.trial.fixation_count(it.no_regressions), 4)

    with it.having('percent regressions measure'):
        @it.should('return the proportion of saccades that are regressions')
        def test_percent_regressions():
            it.assertEqual(measures.trial.percent_regressions(it.trial_x), 1.0/3)
            it.assertEqual(measures.trial.percent_regressions(it.trial_y), 1.0/3)
            it.assertEqual(measures.trial.percent_regressions(it.no_regressions), 0)

    with it.having('trial total time measure'):
        @it.should('return the total time in the trial')
        def test_total_time():
            it.assertEqual(measures.trial.trial_total_time(it.trial_x), 400)
            it.assertEqual(measures.trial.trial_total_time(it.trial_y), 400)
            it.assertEqual(measures.trial.trial_total_time(it.no_regressions), 400)

    with it.having('average forward saccade length measure'):
        @it.should('return the average forward saccade length')
        def test_average_forward_saccade():
            it.assertEqual(measures.trial.average_forward_saccade(it.trial_x), 25)
            it.assertEqual(measures.trial.average_forward_saccade(it.trial_y), 15)
            it.assertEqual(measures.trial.average_forward_saccade(it.no_regressions), 20)

    with it.having('average backward saccade length measure'):
        @it.should('be true if there is a regression into the target region')
        def test_average_backward_saccade():
            it.assertEqual(measures.trial.average_backward_saccade(it.trial_x), 40)
            it.assertEqual(measures.trial.average_backward_saccade(it.trial_y), 30)
            it.assertEqual(measures.trial.average_backward_saccade(it.no_regressions), 0)

it.createTests(globals())
