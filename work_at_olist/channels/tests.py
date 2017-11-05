import unittest

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from django.utils.six import StringIO
from .models import Category, Channel


class ChannelTestCase(TestCase):
    def setUp(self):
        self.channel = Channel.create('FooChannel')

    def test_create_new_channel(self):
        Channel.create('BarChannel')
        self.assertTrue(Channel.objects.filter(name='BarChannel').exists())

    def test_categories_root_is_created(self):
        self.assertIsInstance(self.channel.categories, Category)

    def test_channel_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Channel.objects.create(name='FooChannel')

    def test_add_single_category(self):
        self.channel.add_category(['Home & Garden'])
        self.assertEqual(len(channel.categories.get_children()), 1)

    def test_add_multilevel_categories(self):
        category = [
            'Home & Garden',
            'Household Appliances',
            'Laundry Appliances',
            'Dryers',
        ]
        channel.add_category(category)
        children = channel.categories.get_children()
        self.assertEqual(len(category), len(children))

    def test_add_subcategory_to_existing_category(self):
        category = [
            'Home & Garden',
            'Kitchen & Dining',
            'Kitchen Tools & Utensils',
            'Food Graters & Zesters',
        ]
        channel.add_category(category)
        children = channel.categories.get_children()
        self.assertEqual(len(children), 7)

    def test_no_duplicate_category_on_same_level(self):
        with self.assertRaises(IntegrityError):
            Category.create(name='Home & Garden', parent=self.channel.categories)


@unittest.skip('temporarily skip command tests')
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
