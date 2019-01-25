from nose2.tools import such
from sideeye import measures
from sideeye.data import Point, Fixation, Region, Item, Trial

with such.A('Duration Region Measures') as it:
    @it.has_setup
    def setup_all():
        # /aaaaaaaaaa/aaaaaaaaaa/aaaaaaaaaa/aaaaaaaaaa/
        it.regions_x = [
            Region(Point(0, 0), Point(10, 0)),
            Region(Point(10, 0), Point(20, 0)),
            Region(Point(20, 0), Point(30, 0)),
            Region(Point(30, 0), Point(40, 0))
        ]
        it.item_x = Item(1, 1, it.regions_x)
        it.fixations_x = [
            Fixation(Point(0, 0), 0, 150, 0, it.regions_x[0]),
            Fixation(Point(3, 0), 150, 200, 1, it.regions_x[0]),
            Fixation(Point(22, 0), 200, 350, 2, it.regions_x[2]),
            Fixation(Point(24, 0), 350, 350, 3, it.regions_x[2], excluded=True),
            Fixation(Point(12, 0), 350, 400, 4, it.regions_x[1]),
            Fixation(Point(3, 0), 400, 550, 5, it.regions_x[0]),
            Fixation(Point(11, 0), 550, 600, 6, it.regions_x[1])
        ]
        it.trial_x = Trial(1, 600, it.item_x, it.fixations_x)

        it.fixations_x2 = [
            Fixation(Point(0, 0), 0, 150, 0, it.regions_x[0]),
            Fixation(Point(3, 0), 150, 200, 1, it.regions_x[0]),
            Fixation(Point(22, 0), 200, 370, 2, it.regions_x[2]),
            Fixation(Point(24, 0), 370, 380, 3, it.regions_x[2], excluded=True),
            Fixation(Point(21, 0), 380, 400, 4, it.regions_x[2]),
            Fixation(Point(3, 0), 400, 550, 5, it.regions_x[0])
        ]
        it.trial_x2 = Trial(1, 600, it.item_x, it.fixations_x2)

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
            Fixation(Point(12, 1), 100, 150, 1, it.regions_y[3]),
            Fixation(Point(15, 1), 150, 350, 2, it.regions_y[3]),
            Fixation(Point(8, 0), 350, 400, 3, it.regions_y[0]),
            Fixation(Point(15, 1), 400, 600, 4, it.regions_y[3]),
            Fixation(Point(17, 1), 600, 700, 5, it.regions_y[3])
        ]
        it.trial_y = Trial(1, 400, it.item_y, it.fixations_y)

    with it.having('first_fixation_duration measure'):
        @it.should('calculate first pass fixation duration correctly')
        def test_first_fixation_duration():
            it.assertEqual(measures.region.first_fixation_duration(it.trial_x, 2)['value'], 150)
            it.assertEqual(measures.region.first_fixation_duration(it.trial_y, 1)['value'], 100)
            it.assertEqual(measures.region.first_fixation_duration(it.trial_x, 0)['value'], 150)
            it.assertEqual(measures.region.first_fixation_duration(it.trial_y, 3)['value'], 50)

        @it.should('be None if the region is skipped')
        def test_first_fixation_duration_skip():
            it.assertEqual(measures.region.first_fixation_duration(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.first_fixation_duration(it.trial_y, 2)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_first_fixation_duration_error():
            with it.assertRaises(ValueError):
                measures.region.first_pass_fixation_count(it.trial_x, 5)

    with it.having('single fixation duration measure'):
        @it.should('calculate first pass time correctly')
        def test_single_fixation():
            it.assertEqual(measures.region.single_fixation_duration(it.trial_x, 2)['value'], 150)
            it.assertEqual(measures.region.single_fixation_duration(it.trial_y, 1)['value'], 100)
            it.assertEqual(measures.region.single_fixation_duration(it.trial_x, 0)['value'], None)
            it.assertEqual(measures.region.single_fixation_duration(it.trial_y, 3)['value'], None)

        @it.should('be None if the region is skipped in first pass')
        def test_single_fixation_skip():
            it.assertEqual(measures.region.single_fixation_duration(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.single_fixation_duration(it.trial_y, 2)['value'], None)
            it.assertEqual(measures.region.single_fixation_duration(it.trial_x, 1)['value'], None)
            it.assertEqual(measures.region.single_fixation_duration(it.trial_y, 0)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_single_fixation_error():
            with it.assertRaises(ValueError):
                measures.region.single_fixation_duration(it.trial_x, 5)

    with it.having('first pass time measure'):
        @it.should('calculate first pass time correctly')
        def test_first_pass():
            it.assertEqual(measures.region.first_pass(it.trial_x, 2)['value'], 150)
            it.assertEqual(measures.region.first_pass(it.trial_y, 1)['value'], 100)
            it.assertEqual(measures.region.first_pass(it.trial_x, 0)['value'], 200)
            it.assertEqual(measures.region.first_pass(it.trial_y, 3)['value'], 250)

        @it.should('be None if the region is skipped in first pass')
        def test_first_pass_skip():
            it.assertEqual(measures.region.first_pass(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.first_pass(it.trial_y, 2)['value'], None)
            it.assertEqual(measures.region.first_pass(it.trial_x, 1)['value'], None)
            it.assertEqual(measures.region.first_pass(it.trial_y, 0)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_first_pass_error():
            with it.assertRaises(ValueError):
                measures.region.first_pass(it.trial_x, 5)

    with it.having('go-past time measure'):
        @it.should('calculate go-past time correctly')
        def test_go_past_time():
            it.assertEqual(measures.region.go_past(it.trial_x, 2)['value'], 400)
            it.assertEqual(measures.region.go_past(it.trial_y, 1)['value'], 100)
            it.assertEqual(measures.region.go_past(it.trial_x, 0)['value'], 200)
            it.assertEqual(measures.region.go_past(it.trial_y, 3)['value'], 600)

        @it.should('be None if the region is skipped in first pass')
        def test_go_past_time_skip():
            it.assertEqual(measures.region.go_past(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.go_past(it.trial_y, 2)['value'], None)
            it.assertEqual(measures.region.go_past(it.trial_x, 1)['value'], None)
            it.assertEqual(measures.region.go_past(it.trial_y, 0)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_go_past_time_error():
            with it.assertRaises(ValueError):
                measures.region.go_past(it.trial_x, 5)

    with it.having('total time measure'):
        @it.should('calculate total time correctly')
        def test_total_time():
            it.assertEqual(measures.region.total_time(it.trial_x, 1)['value'], 100)
            it.assertEqual(measures.region.total_time(it.trial_y, 0)['value'], 50)
            it.assertEqual(measures.region.total_time(it.trial_x, 0)['value'], 350)
            it.assertEqual(measures.region.total_time(it.trial_y, 3)['value'], 550)

        @it.should('be 0 if the region is skipped')
        def test_total_time_skip():
            it.assertEqual(measures.region.total_time(it.trial_x, 3)['value'], 0)
            it.assertEqual(measures.region.total_time(it.trial_y, 2)['value'], 0)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_total_time_error():
            with it.assertRaises(ValueError):
                measures.region.total_time(it.trial_x, 5)

    with it.having('right-bounded time measure'):
        @it.has_test_setup
        def setup_rb():
            it.right_bounded_fixations = [
                Fixation(Point(0, 0), 0, 150, 0, it.regions_x[0]),
                Fixation(Point(3, 0), 150, 200, 1, it.regions_x[0]),
                Fixation(Point(14, 0), 200, 350, 2, it.regions_x[1]),
                Fixation(Point(12, 0), 350, 400, 3, it.regions_x[1]),
                Fixation(Point(3, 0), 400, 550, 4, it.regions_x[0]),
                Fixation(Point(11, 0), 550, 600, 5, it.regions_x[1]),
                Fixation(Point(21, 0), 650, 700, 6, it.regions_x[2]),
                Fixation(Point(11, 0), 750, 800, 7, it.regions_x[1])
            ]
            it.trial_right_bound = Trial(1, 600, it.item_x, it.right_bounded_fixations)

        @it.should('calculate right-bounded time correctly')
        def test_right_bounded_time():
            it.assertEqual(
                measures.region.right_bounded_time(it.trial_right_bound, 0)['value'],
                200
            )
            it.assertEqual(
                measures.region.right_bounded_time(it.trial_right_bound, 1)['value'],
                250
            )

        @it.should('be None if the region is skipped during first pass')
        def test_right_bounded_time_skip():
            it.assertEqual(
                measures.region.right_bounded_time(it.trial_right_bound, 3)['value'],
                None
            )
            it.assertEqual(measures.region.right_bounded_time(it.trial_y, 0)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_right_bounded_time_error():
            with it.assertRaises(ValueError):
                measures.region.right_bounded_time(it.trial_x, 5)

    with it.having('reread time measure'):
        @it.should('calculate reread time correctly')
        def test_reread_time():
            it.assertEqual(measures.region.reread_time(it.trial_x, 0)['value'], 150)

        @it.should('be 0 if the region is skipped or not reread')
        def test_reread_time_skip():
            it.assertEqual(measures.region.reread_time(it.trial_x, 3)['value'], 0)
            it.assertEqual(measures.region.reread_time(it.trial_y, 2)['value'], 0)
            it.assertEqual(measures.region.reread_time(it.trial_x, 2)['value'], 0)
            it.assertEqual(measures.region.reread_time(it.trial_y, 1)['value'], 0)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_reread_time_error():
            with it.assertRaises(ValueError):
                measures.region.reread_time(it.trial_x, 5)

    with it.having('second pass time measure'):
        @it.should('calculate second pass time correctly')
        def test_second_pass_time():
            it.assertEqual(measures.region.second_pass(it.trial_x, 0)['value'], 150)
            it.assertEqual(measures.region.second_pass(it.trial_x, 1)['value'], 50)

        @it.should('be 0 if the region is skipped or not reread')
        def test_second_pass_time_skip():
            it.assertEqual(measures.region.second_pass(it.trial_x, 3)['value'], 0)
            it.assertEqual(measures.region.second_pass(it.trial_y, 2)['value'], 0)
            it.assertEqual(measures.region.second_pass(it.trial_x, 2)['value'], 0)
            it.assertEqual(measures.region.second_pass(it.trial_y, 1)['value'], 0)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_second_pass_error():
            with it.assertRaises(ValueError):
                measures.region.second_pass(it.trial_x, 5)

    with it.having('spillover time measure'):
        @it.should('calculate spillover time correctly')
        def test_spillover_time():
            it.assertEqual(measures.region.spillover_time(it.trial_x, 0)['value'], 50)

        @it.should('be None if there are no fixations in the spillover region')
        def test_spillover_time_skip():
            it.assertEqual(measures.region.spillover_time(it.trial_x, 2)['value'], None)
            it.assertEqual(measures.region.spillover_time(it.trial_y, 1)['value'], None)
            it.assertEqual(measures.region.spillover_time(it.trial_y, 0)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_spillover_time_error():
            with it.assertRaises(ValueError):
                measures.region.spillover_time(it.trial_x, 5)

    with it.having('refixation time measure'):
        @it.should('calculate refixation time correctly')
        def test_refixation_time():
            it.assertEqual(measures.region.refixation_time(it.trial_x, 0)['value'], 50)
            it.assertEqual(measures.region.refixation_time(it.trial_y, 3)['value'], 200)

        @it.should('be None if the region is skipped')
        def test_refixation_time_skip():
            it.assertEqual(measures.region.refixation_time(it.trial_x, 3)['value'], None)
            it.assertEqual(measures.region.refixation_time(it.trial_y, 2)['value'], None)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_refixation_time_error():
            with it.assertRaises(ValueError):
                measures.region.refixation_time(it.trial_x, 5)

    with it.having('go back time by character measure'):
        @it.should('calculate refixation time correctly')
        def test_go_back_time_char():
            it.assertEqual(measures.region.go_back_time_char(it.trial_x2, 0)['value'], 370)
            it.assertEqual(measures.region.go_back_time_char(it.trial_x, 0)['value'], 350)
            it.assertEqual(measures.region.go_back_time_char(it.trial_y, 3)['value'], 250)

        @it.should('measures from the previous fixation if the region is skipped')
        def test_refixation_char_time_skip():
            it.assertEqual(measures.region.go_back_time_char(it.trial_x2, 1)['value'], 170)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_go_back_time_char_error():
            with it.assertRaises(ValueError):
                measures.region.go_back_time_char(it.trial_x, 5)

    with it.having('go back time by region measure'):
        @it.should('calculate refixation time correctly')
        def test_go_back_time_region():
            it.assertEqual(measures.region.go_back_time_region(it.trial_x, 0)['value'], 350)
            it.assertEqual(measures.region.go_back_time_region(it.trial_y, 3)['value'], 250)

        @it.should('measures from the previous fixation if the region is skipped')
        def test_go_back_time_region_skip():
            it.assertEqual(measures.region.go_back_time_region(it.trial_y, 2)['value'], 250)

        @it.should('throw an error if the target region does not exist in the trial')
        def test_go_back_time_region_error():
            with it.assertRaises(ValueError):
                measures.region.go_back_time_region(it.trial_x, 5)

it.createTests(globals())
