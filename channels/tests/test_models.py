from django.test import TestCase
from django.core.exceptions import ValidationError
from channels.models import Channel, Category


class ChannelCategoriesInsertionTestCase(TestCase):
    def setUp(self):
        """setup the channel used by unit tests"""
        self.channel = Channel.objects.create(name='FooChannel')

    def test_channel_is_inserted_to_db(self):
        self.assertTrue(Channel.objects.filter(name='FooChannel').exists())

    def test_channel_name_must_be_unique(self):
        with self.assertRaises(ValidationError):
            Channel.objects.create(name='FooChannel')

    def test_channel_name_unique_case_insensitive(self):
        with self.assertRaises(ValidationError):
            Channel.objects.create(name='foochannel')

    def test_add_single_category(self):
        category = ['Home & Garden']
        self.channel.add_category(category)
        children_count = self.channel.get_descendant_count()
        self.assertEqual(children_count, 1)

    def test_add_multilevel_categories(self):
        category = [
            'Home & Garden',
            'Household Appliances',
            'Laundry Appliances',
            'Dryers',
        ]
        self.channel.add_category(category)
        children_count = self.channel.get_descendant_count()
        self.assertEqual(children_count, len(category))

    def test_add_subcategory_to_existing_category(self):
        categories = [
            ['Home & Garden',  # common ancestor
             'Kitchen & Dining',
             'Kitchen Tools & Utensils',
             'Food Graters & Zesters'],
            ['Home & Garden',
             'Household Appliances',
             'Laundry Appliances',
             'Dryers'],
        ]

        for category in categories:
            self.channel.add_category(category)

        children_count = len(self.channel.get_family())
        self.assertEqual(children_count, 7)

    def test_no_duplicate_category_on_same_level(self):
        with self.assertRaises(ValidationError):
            Category.objects.create(name='Home & Garden',
                                    parent=self.channel)
            Category.objects.create(name='Home & Garden',
                                    parent=self.channel)

    def test_strip_white_spaces(self):
        category = [
            '  Home & Garden  ',
            '        Household Appliances',
            'Laundry Appliances ',
            '  Dryers '
        ]
        expected = [
            '/FooChannel/Home & Garden',
            '/FooChannel/Home & Garden/Household Appliances',
            '/FooChannel/Home & Garden/Household Appliances/Laundry Appliances',
            '/FooChannel/Home & Garden/Household Appliances/Laundry Appliances/Dryers',
        ]
        self.channel.add_category(category)
        channel_categories = [c.path for c in self.channel.subcategories]
        self.assertEqual(channel_categories, expected)


class ChannelCategoriesRetrievalTestCase(TestCase):
    def setUp(self):
        categories = [
            ['Home & Garden',
             'Kitchen & Dining',
             'Kitchen Tools & Utensils',
             'Food Graters & Zesters'],
            ['Home & Garden',
             'Household Appliances',
             'Laundry Appliances',
             'Dryers'],
        ]
        self.channel = Channel.objects.create(name='FooChannel')
        for category in categories:
            self.channel.add_category(category)
        self.channel.refresh_from_db()

    def test_get_categories_count(self):
        count = self.channel.subcategories_count
        self.assertEqual(count, 7)

    def test_get_all_categories(self):
        """
        all categories should return a queryset
        """
        expected = set(Category.objects.filter(tree_id=self.channel.tree_id))
        categories = set(self.channel.subcategories)
        self.assertEqual(categories, expected)

    def test_get_specific_category_path(self):
        expected = '/FooChannel/Home & Garden/Household Appliances/Laundry Appliances'
        path = self.channel.get_category('Laundry Appliances').path
        self.assertEqual(path, expected)

    def test_get_root_category_path(self):
        expected = '/FooChannel/Home & Garden'
        path = self.channel.get_category('Home & Garden').path
        self.assertEqual(path, expected)
