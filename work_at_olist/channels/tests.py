from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from .models import Category, Channel

from django.core.management.base import CommandError

class CategoryTestCase(TestCase):
    def setUp(self):
        pass

    def test_insert_single_category(self):
        pass

    def test_insert_many_categories(self):
        pass

    def test_retrieve_categories(self):
        pass

    def output_all_categories_from_channel(self):
        pass


class ChannelTestsCase(TestCase):
    def setUp(self):
        pass

    def test_add_new_channel(self):
        pass

    def test_retrieve_channel_categories(self):
        pass


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
