import unittest

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from django.utils.six import StringIO
from .models import Channel


class ChannelCategoriesInsertionTestCase(TestCase):
    def setUp(self):
        """setup the channel used by unit tests"""
        self.channel = Channel.create('FooChannel')

    def test_channel_is_inserted_to_db(self):
        self.assertTrue(Channel.objects.filter(name='FooChannel').exists())

    def test_channel_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Channel.objects.create(name='FooChannel')

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

    def test_no_duplicate_category_on_same_tree(self):
        with self.assertRaises(IntegrityError):
            Channel.objects.create(name='Home & Garden',
                                    parent=self.channel)
            Channel.objects.create(name='Home & Garden',
                                    parent=self.channel)


class ChannelCategoriesRetrievalTestCare(TestCase):
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
        self.channel = Channel.create('foo')

        for category in categories:
            self.channel.add_category(category)

    def test_get_categories_count(self):
        count = self.channel.get_categories_count()
        self.assertEqual(count, 7)

    def test_get_all_categories_full_paths(self):
        """
        all categories should return a list of paths to each
        category ordered by name
        """
        expected = [
            'Home & Garden',
            'Home & Garden/Household Appliances',
            'Home & Garden/Household Appliances/Laundry Appliances',
            'Home & Garden/Household Appliances/Laundry Appliances/Dryers',
            'Home & Garden/Kitchen & Dining',
            'Home & Garden/Kitchen & Dining/Kitchen Tools & Utensils',
            'Home & Garden/Kitchen & Dining/Kitchen Tools & Utensils/Food Graters & Zesters',
        ]
        paths = self.channel.get_all_categories()
        self.assertEqual(paths, expected)

    def test_get_specific_category_path(self):
        expected = 'Home & Garden/Household Appliances/Laundry Appliances'
        path = self.channel.get_category('Laundry Appliances').path
        self.assertEqual(path, expected)

    def test_get_root_category_path(self):
        expected = 'Home & Garden'
        path = self.channel.get_category('Home & Garden').path
        self.assertEqual(path, expected)


class ImportCategoriesTest(TestCase):
    def test_non_existing_file(self):
        out = StringIO()
        call_command('importcategories', 'foo', 'bar', stderr=out)
        self.assertIn('File bar not found.', out.getvalue())

    def test_required_args(self):
        with self.assertRaises(CommandError):
            call_command('importcategories')

    def test_succesfully_add_channel_categories(self):
        out = StringIO()
        file = 'test_data/test_data_sample_0.csv'
        call_command('importcategories', 'foo', file, stdout=out)
        expected = 'Channel foo updated with 10 categories from file: {}'.format(file)
        self.assertIn(expected, out.getvalue())

    def test_custom_separator_in_file(self):
        out = StringIO()
        file = 'test_data/test_data_sample_commas.csv'
        call_command('importcategories', '--sep=","', 'foo', file, stdout=out)
        expected = 'Channel foo updated with 10 categories from file: {}'.format(file)
        self.assertIn(expected, out.getvalue())

    def test_skip_empty_lines(self):
        file = 'test_data/test_data_sample_empty_lines.csv'
        call_command('importcategories', 'foo', file)
        expected = [
            'Business & Industrial',
            'Business & Industrial/Advertising & Marketing',
            'Business & Industrial/Advertising & Marketing/Trade Show Displays',
            'Home & Garden',
            'Home & Garden/Smoking Accessories',
            'Home & Garden/Smoking Accessories/Ashtrays',
            'Sporting Goods',
            'Sporting Goods/Outdoor Recreation',
            'Sporting Goods/Outdoor Recreation/Boating & Water Sports',
            'Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting',
            'Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting/Boating Gloves',
        ]
        channel = Channel.objects.get(name='foo')
        self.assertEqual(channel.get_all_categories(), expected)

    def test_data_is_actually_added(self):
        file = 'test_data/test_data_sample_0.csv'
        call_command('importcategories', 'foo', file)
        expected = [
            'Business & Industrial',
            'Business & Industrial/Advertising & Marketing',
            'Business & Industrial/Advertising & Marketing/Trade Show Displays',
            'Electronics',
            'Electronics/Print, Copy, Scan & Fax',
            'Electronics/Print, Copy, Scan & Fax/Printer, Copier & Fax Machine Accessories',
            'Electronics/Print, Copy, Scan & Fax/Printer, Copier & Fax Machine Accessories/Printer Consumables',
            'Electronics/Print, Copy, Scan & Fax/Printer, Copier & Fax Machine Accessories/Printer Consumables/Printer Drums & Drum Kits',
            'Health & Beauty',
            'Health & Beauty/Personal Care',
            'Health & Beauty/Personal Care/Cosmetics',
            'Health & Beauty/Personal Care/Cosmetics/Makeup',
            'Health & Beauty/Personal Care/Cosmetics/Makeup/Face Makeup',
            'Health & Beauty/Personal Care/Cosmetics/Makeup/Face Makeup/Highlighters & Luminizers',
            'Home & Garden',
            'Home & Garden/Kitchen & Dining',
            'Home & Garden/Kitchen & Dining/Kitchen Appliances',
            'Home & Garden/Kitchen & Dining/Kitchen Appliances/Frozen Drink Makers',
            'Home & Garden/Kitchen & Dining/Kitchen Tools & Utensils',
            'Home & Garden/Kitchen & Dining/Kitchen Tools & Utensils/Mashers',
            'Home & Garden/Kitchen & Dining/Tableware',
            'Home & Garden/Kitchen & Dining/Tableware/Flatware',
            'Home & Garden/Kitchen & Dining/Tableware/Flatware/Chopstick Accessories',
            'Home & Garden/Smoking Accessories',
            'Home & Garden/Smoking Accessories/Ashtrays',
            'Sporting Goods',
            'Sporting Goods/Outdoor Recreation',
            'Sporting Goods/Outdoor Recreation/Boating & Water Sports',
            'Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting',
            'Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting/Boating Gloves',
            'Vehicles & Parts',
            'Vehicles & Parts/Vehicle Parts & Accessories',
            'Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Maintenance, Care & Decor',
            'Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Maintenance, Care & Decor/Vehicle Decor',
            'Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Maintenance, Care & Decor/Vehicle Decor/Vehicle Hitch Covers',
            'Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Safety & Security',
            'Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Safety & Security/Vehicle Alarms & Locks',
            'Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Safety & Security/Vehicle Alarms & Locks/Vehicle Door Locks & Parts'
         ]
        channel = Channel.objects.get(name='foo')
        self.assertEqual(channel.get_all_categories(), expected)
