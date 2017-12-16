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

    def test_data_is_actually_added(self):
        file = 'test_data/test_data_sample_0.csv'
        call_command('importcategories', 'FooChannel', file)
        channel = Channel.objects.get(name='FooChannel')
        self.assertEqual(channel.subcategories_count, 38)

    def test_skip_empty_lines(self):
        file = 'test_data/test_data_sample_empty_lines.csv'
        call_command('importcategories', 'FooChannel', file)
        channel = Channel.objects.get(name='FooChannel')
        self.assertEqual(channel.subcategories_count, 11)
