import unittest

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from django.utils.six import StringIO
from .models import CategoryTree, Channel


class ChannelCategoriesInsertionTestCase(TestCase):
    def setUp(self):
        """setup the channel used by unit tests"""
        self.channel = Channel.create('FooChannel')

    def test_channel_is_inserted_to_db(self):
        self.assertTrue(Channel.objects.filter(name='FooChannel').exists())

    def test_categories_root_is_created(self):
        """check if the channel's categories relation is added automatically"""
        self.assertIsInstance(self.channel.categories, CategoryTree)

    def test_categories_root_naming(self):
        """
        when automatically creating a category root
        for a channel, append '_root' to channel's name.
        This helps when using admin pages, and shell.
        """
        self.assertTrue(self.channel.categories.name.endswith('_root'))

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

    def test_no_duplicate_category_on_same_tree(self):
        with self.assertRaises(IntegrityError):
            CategoryTree.objects.create(name='Home & Garden',
                                    parent=self.channel.categories)
            CategoryTree.objects.create(name='Home & Garden',
                                    parent=self.channel.categories)


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
            ['Home & Garden'],
            ['Home & Garden', 'Household Appliances'],
            ['Home & Garden', 'Household Appliances', 'Laundry Appliances'],
            ['Home & Garden', 'Household Appliances', 'Laundry Appliances', 'Dryers'],
            ['Home & Garden', 'Kitchen & Dining'],
            ['Home & Garden', 'Kitchen & Dining', 'Kitchen Tools & Utensils'],
            ['Home & Garden', 'Kitchen & Dining', 'Kitchen Tools & Utensils', 'Food Graters & Zesters']
        ]
        paths = self.channel.get_all_categories()
        self.assertEqual(paths, expected)

    def test_get_specific_category_path(self):
        expected = ['Home & Garden', 'Household Appliances', 'Laundry Appliances']
        path = self.channel.get_category('Laundry Appliances')
        self.assertEqual(path, expected)

    def test_get_root_category_path(self):
        expected = ['Home & Garden']
        path = self.channel.get_category('Home & Garden')
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
