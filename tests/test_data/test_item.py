from nose2.tools import such
from sideeye import Point, Region, Item

with such.A('Item') as it:
    @it.has_test_setup
    def setup():
        it.r1 = Region(Point(1, 1), Point(3, 1), 1, 'region 1')
        it.r2 = Region(Point(3, 1), Point(8, 1), 1, 'region 2')
        it.r3 = Region(Point(8, 1), Point(2, 2), 1, 'region 3')
        it.r4 = Region(Point(1, 1), Point(3, 1), 1, 'region 1')
        it.r5 = Region(Point(3, 1), Point(8, 1), 1, 'region 2')
        it.r6 = Region(Point(8, 1), Point(2, 2), 1, 'region 3')
        it.labeled_item = Item(1, 1, [it.r1, it.r2, it.r3], ['r1', 'r2', 'r3'])
        it.unlabeled_item = Item(2, 1, [it.r4, it.r5, it.r6])

    @it.should('label each region with provided labels')
    def test_provided_labels():
        it.assertEqual(it.labeled_item.regions[0].label, 'r1')
        it.assertEqual(it.labeled_item.regions[1].label, 'r2')
        it.assertEqual(it.labeled_item.regions[2].label, 'r3')

    @it.should('label each region with a number')
    def test_labeling():
        it.assertEqual(it.unlabeled_item.regions[0].label, 0)
        it.assertEqual(it.unlabeled_item.regions[1].label, 1)
        it.assertEqual(it.unlabeled_item.regions[2].label, 2)

    @it.should('get the region with the corresponding label')
    def test_get_region():
        it.assertEqual(it.labeled_item.get_region('r1'), it.r1)
        it.assertEqual(it.unlabeled_item.get_region(2), it.r6)

    @it.should('get the region containing the specified position')
    def test_find_region():
        it.assertEqual(it.labeled_item.find_region(1, 1), it.r1)
        it.assertEqual(it.labeled_item.find_region(9, 1), it.r3)

    @it.should('get the number of regions in the item')
    def test_region_count():
        it.assertEqual(it.labeled_item.region_count(), 3)

    @it.should('not allow items with a different number of regions and labels')
    def test_region_label_validation():
        with it.assertRaises(ValueError):
            Item(1, 1, [it.r1, it.r2, it.r3], ['region 1', 'region 2'])

    @it.should('not allow items with repeated labels')
    def test_label_uniqueness():
        with it.assertRaises(ValueError):
            Item(1, 1, [it.r1, it.r2, it.r3], ['r1', 'r1', 'r3'])

    @it.should('not allow items with no regions')
    def test_region_existence():
        with it.assertRaises(ValueError):
            Item(1, 1, [])

    @it.should('not allow items with repeated regions')
    def test_region_uniqueness():
        with it.assertRaises(ValueError):
            Item(1, 1, [it.r1, it.r1, it.r1])

    @it.should('have equality defined correctly')
    def test_item_equality():
        it.assertTrue(Item(2, 1, [it.r1, it.r2, it.r3]) == Item(2, 1, [it.r1, it.r2, it.r3]))
        it.assertTrue(
            Item(2, 1, [it.r1, it.r2, it.r3]) !=
            Item(2, 1, [it.r1, it.r2, Region(Point(1, 1), Point(2, 2), 1, 'region 4')])
        )

it.createTests(globals())
