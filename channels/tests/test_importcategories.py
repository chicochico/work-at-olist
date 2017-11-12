import unittest

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils.six import StringIO
from channels.models import Channel


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
