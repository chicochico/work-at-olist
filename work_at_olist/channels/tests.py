from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from django.utils.six import StringIO
from .models import Category



class CategoryTestCase(TestCase):
    def test_add_new_channel(self):
        # the root of a tree represents a channel
        channel = Category.objects.create(name='FooChannel')
        all_channels = Category.objects.root_nodes()
        self.assertIn(all_channels, channel)

    def test_add_single_category(self):
        channel = Category.objects.get(name='FooChannel')
        Category.objects.create(name='Home & Garden', parent=channel)
        self.assertEqual(len(channel.get_children()), 1)

    def test_add_multilevel_categories(self):
        category = [
            'Home & Garden',
            'Household Appliances',
            'Laundry Appliances',
            'Dryers',
        ]
        channel = Category.objects.get(name='FooChannel', parent=None)
        channel.add_category(category)
        children = channel.get_children()
        self.assertEqual(len(category), len(children))

    def test_add_subcategory_to_existing_category(self):
        category = [
            'Home & Garden',
            'Kitchen & Dining',
            'Kitchen Tools & Utensils',
            'Food Graters & Zesters',
        ]
        channel = Category.objects.get(name='FooChannel')
        channel.add_category(category)
        children = channel.get_children()
        self.assertEqual(len(children), 7)

    def test_channel_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='FooChannel')

    def test_no_duplicate_category_on_same_level(self):
        with self.assertRaises(IntegrityError):
            channel = Category.objects.get(name='FooChannel', parent=None)
            Channel.objects.create(name='Home & Garden', parent=channel)


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
