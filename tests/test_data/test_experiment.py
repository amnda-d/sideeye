from nose2.tools import such
from sideeye import Point, Fixation, Region, Item, Trial, Experiment

with such.A('Experiment') as it:
    @it.has_setup
    def setup():
        it.r1 = Region(Point(1, 1), Point(2, 2), 1, 'region 1')
        it.r2 = Region(Point(1, 1), Point(2, 2), 1, 'region 2')
        it.r3 = Region(Point(1, 1), Point(2, 2), 1, 'region 3')
        it.fix1 = Fixation(Point(1, 2), 3, 4, 0, 'region')
        it.fix2 = Fixation(Point(1, 2), 5, 6, 1, 'region')
        it.fix3 = Fixation(Point(1, 3), 8, 9, 2, 'region')
        it.item = Item(1, 1, [it.r1, it.r2, it.r3])
        it.item2 = Item(2, 1, [it.r1, it.r3])
        it.trial = Trial(1, 4, it.item, [it.fix1, it.fix2, it.fix3])
        it.trial2 = Trial(2, 4, it.item2, [it.fix1, it.fix3])
        it.experiment = Experiment('ex1', [it.trial, it.trial2], filename='ex1.da1')

    @it.should('get the correct trial by item number and condition')
    def test_get_item():
        it.assertEqual(it.experiment.get_trial(2, 1), it.trial2)

    @it.should('get the correct trial by index')
    def test_get_by_index():
        it.assertEqual(it.experiment.get_trial(index=1), it.trial)

    @it.should('require either item number and condition or trial index to get trial')
    def test_get_trial_validation():
        with it.assertRaises(ValueError):
            it.experiment.get_trial(1)

        with it.assertRaises(ValueError):
            it.experiment.get_trial()

    @it.should('have equality defined correctly')
    def test_experiment_equality():
        it.assertTrue(
            Experiment('ex1', [it.trial, it.trial2], filename='ex1.da1', date=1) ==
            Experiment('ex1', [it.trial, it.trial2], filename='ex1.da1', date=1)
        )
        it.assertTrue(
            Experiment('ex1', [it.trial, it.trial2], filename='ex1.da1') !=
            Experiment('ex2', [it.trial], filename='ex2.da1')
        )

it.createTests(globals())
