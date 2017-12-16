from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils.six import StringIO
from channels.models import Channel


class ImportCategoriesTest(TestCase):
    def test_non_existing_file(self):
        out = StringIO()
        call_command('importcategories', 'FooChannel', 'bar', stderr=out)
        self.assertIn('File bar not found.', out.getvalue())

    def test_required_args(self):
        with self.assertRaises(CommandError):
            call_command('importcategories')

    def test_succesfully_add_channel_categories(self):
        out = StringIO()
        file = 'test_data/test_data_sample_0.csv'
        call_command('importcategories', 'FooChannel', file, stdout=out)
        expected = 'Channel FooChannel updated with 10 categories from file: {}'.format(file)
        self.assertIn(expected, out.getvalue())

    def test_custom_separator_in_file(self):
        out = StringIO()
        file = 'test_data/test_data_sample_commas.csv'
        call_command('importcategories', '--sep=","', 'FooChannel', file, stdout=out)
        expected = 'Channel FooChannel updated with 10 categories from file: {}'.format(file)
        self.assertIn(expected, out.getvalue())

    def test_skip_empty_lines(self):
        file = 'test_data/test_data_sample_empty_lines.csv'
        call_command('importcategories', 'FooChannel', file)
        expected = [
            '/FooChannel/Business & Industrial',
            '/FooChannel/Business & Industrial/Advertising & Marketing',
            '/FooChannel/Business & Industrial/Advertising & Marketing/Trade Show Displays',
            '/FooChannel/Home & Garden',
            '/FooChannel/Home & Garden/Smoking Accessories',
            '/FooChannel/Home & Garden/Smoking Accessories/Ashtrays',
            '/FooChannel/Sporting Goods',
            '/FooChannel/Sporting Goods/Outdoor Recreation',
            '/FooChannel/Sporting Goods/Outdoor Recreation/Boating & Water Sports',
            '/FooChannel/Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting',
            '/FooChannel/Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting/Boating Gloves',
        ]
        channel = Channel.objects.get(name='FooChannel')
        self.assertEqual(channel.get_all_categories_paths(), expected)

    def test_data_is_actually_added(self):
        file = 'test_data/test_data_sample_0.csv'
        call_command('importcategories', 'FooChannel', file)
        expected = [
            '/FooChannel/Business & Industrial',
            '/FooChannel/Business & Industrial/Advertising & Marketing',
            '/FooChannel/Business & Industrial/Advertising & Marketing/Trade Show Displays',
            '/FooChannel/Electronics',
            '/FooChannel/Electronics/Print, Copy, Scan & Fax',
            '/FooChannel/Electronics/Print, Copy, Scan & Fax/Printer, Copier & Fax Machine Accessories',
            '/FooChannel/Electronics/Print, Copy, Scan & Fax/Printer, Copier & Fax Machine Accessories/Printer Consumables',
            '/FooChannel/Electronics/Print, Copy, Scan & Fax/Printer, Copier & Fax Machine Accessories/Printer Consumables/Printer Drums & Drum Kits',
            '/FooChannel/Health & Beauty',
            '/FooChannel/Health & Beauty/Personal Care',
            '/FooChannel/Health & Beauty/Personal Care/Cosmetics',
            '/FooChannel/Health & Beauty/Personal Care/Cosmetics/Makeup',
            '/FooChannel/Health & Beauty/Personal Care/Cosmetics/Makeup/Face Makeup',
            '/FooChannel/Health & Beauty/Personal Care/Cosmetics/Makeup/Face Makeup/Highlighters & Luminizers',
            '/FooChannel/Home & Garden',
            '/FooChannel/Home & Garden/Kitchen & Dining',
            '/FooChannel/Home & Garden/Kitchen & Dining/Kitchen Appliances',
            '/FooChannel/Home & Garden/Kitchen & Dining/Kitchen Appliances/Frozen Drink Makers',
            '/FooChannel/Home & Garden/Kitchen & Dining/Kitchen Tools & Utensils',
            '/FooChannel/Home & Garden/Kitchen & Dining/Kitchen Tools & Utensils/Mashers',
            '/FooChannel/Home & Garden/Kitchen & Dining/Tableware',
            '/FooChannel/Home & Garden/Kitchen & Dining/Tableware/Flatware',
            '/FooChannel/Home & Garden/Kitchen & Dining/Tableware/Flatware/Chopstick Accessories',
            '/FooChannel/Home & Garden/Smoking Accessories',
            '/FooChannel/Home & Garden/Smoking Accessories/Ashtrays',
            '/FooChannel/Sporting Goods',
            '/FooChannel/Sporting Goods/Outdoor Recreation',
            '/FooChannel/Sporting Goods/Outdoor Recreation/Boating & Water Sports',
            '/FooChannel/Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting',
            '/FooChannel/Sporting Goods/Outdoor Recreation/Boating & Water Sports/Boating & Rafting/Boating Gloves',
            '/FooChannel/Vehicles & Parts',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Maintenance, Care & Decor',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Maintenance, Care & Decor/Vehicle Decor',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Maintenance, Care & Decor/Vehicle Decor/Vehicle Hitch Covers',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Safety & Security',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Safety & Security/Vehicle Alarms & Locks',
            '/FooChannel/Vehicles & Parts/Vehicle Parts & Accessories/Vehicle Safety & Security/Vehicle Alarms & Locks/Vehicle Door Locks & Parts'
         ]
        channel = Channel.objects.get(name='FooChannel')
        self.assertEqual(channel.get_all_categories_paths(), expected)
