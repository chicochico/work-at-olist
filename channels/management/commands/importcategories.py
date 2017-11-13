from django.core.management.base import BaseCommand, CommandError
from channels.models import Channel

import random

class Command(BaseCommand):
    help = 'Add categories from comma separated file to channel.'

    def add_arguments(self, parser):
        """
        Add the arguments this command accepts
        """
        parser.add_argument(
            'channel',
            type=str,
            help='Name for the channel.')

        parser.add_argument(
            'file',
            help='File location.',
            type=str)

        parser.add_argument(
            '--sep',
            dest='separator',
            default=';',
            help='Specify the separator used in the input file default is (,).',
            type=str)

    def handle(self, *args, **options):
        """
        Do the work
        """
        try:
            categories = self.parse_file(options['file'], options['separator'])
        except FileNotFoundError:
            error_msg = self.style.ERROR(
                'File {} not found.'.format(options['file'])
            )
            self.stderr.write(error_msg)
            return

        # get channel or insert new if it doesnt exist
        channel, _ = Channel.objects.get_or_create(name=options['channel'])
        # delete all existing categories from channel
        channel.delete()
        # create new channel root
        channel.save()

        for category in categories:
            channel.add_category(category)

        ok_str = 'Channel {} updated with {} categories from file: {}'
        ok_msg = self.style.SUCCESS(ok_str.format(options['channel'],
                                                  len(categories),
                                                  options['file']))
        self.stdout.write(ok_msg)


    def parse_file(self, file, separator):
        """
        Parse a file and returns a list of lists, each list
        is the full path to a category.
        """
        try:
            data = open(file, 'r').read().splitlines()
            return [s.split(separator) for s in data if s != '']
        except FileNotFoundError:
            raise


