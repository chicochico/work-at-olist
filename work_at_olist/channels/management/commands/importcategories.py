from django.core.management.base import BaseCommand, CommandError
from channels.models import Category, Channel

import random

class Command(BaseCommand):
    help = 'Add categories from comma separated file to channel.'

    def add_arguments(self, parser):
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
        try:
            categories = self.parse_file(options['file'], options['separator'])

            # get channel or insert new if it doesnt exist
            try:
                channel = Channel.objects.get(name=options['channel'])
            except channel.models.DoesNotExist:
                channel = Channel(options['channel'])
                channel.save()

            for category in categories:
                Category.add(category, channel)

            ok_str = 'Channel {} updated with {} categories from file: {}'
            ok_msg = self.style.SUCCESS(ok_str.format(options['channel'],
                                                      len(categories),
                                                      options['file']))
            self.stdout.write(ok_msg)
        except FileNotFoundError:
            error_msg = self.style.ERROR(
                'File {} not found.'.format(options['file'])
            )
            self.stderr.write(error_msg)


    def parse_file(self, file, separator):
        '''
        parse a file and returns a list of lists, each list
        is the full path to a category.
        '''
        try:
            data = open(file, 'r').read().splitlines()
            return [s.split(separator) for s in data]
        except FileNotFoundError:
            raise


