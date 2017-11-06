import unittest

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from django.utils.six import StringIO
from .models import Category, Channel


class ChannelTestCase(TestCase):
    def setUp(self):
        """setup the channel used by unit tests"""
        self.channel = Channel.create('FooChannel')

    def test_channel_is_inserted_to_db(self):
        self.assertTrue(Channel.objects.filter(name='FooChannel').exists())

    def test_categories_root_is_created(self):
        """check if the channel's categories relation is added automatically"""
        self.assertIsInstance(self.channel.categories, Category)

    def test_channel_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Channel.objects.create(name='FooChannel')

    def test_add_single_category(self):
        category = ['Home & Garden']
        self.channel.add_category(category)
        children_count = self.channel.categories.get_descendant_count()
        self.assertEqual(children_count, 1)

    def test_add_multilevel_categories(self):
        category = [
            'Home & Garden',
            'Household Appliances',
            'Laundry Appliances',
            'Dryers',
        ]
        self.channel.add_category(category)
        children_count = self.channel.categories.get_descendant_count()
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

        children_count = len(self.channel.categories.get_family())
        self.assertEqual(children_count, 7)

    def test_no_duplicate_category_on_same_level(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Home & Garden',
                                    parent=self.channel.categories)
            Category.objects.create(name='Home & Garden',
                                    parent=self.channel.categories)


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
