from django.core.management.base import BaseCommand
from books.models import Author, Book, Genre, Publisher
import csv
from pprint import pprint
from django.utils.text import slugify


class Command(BaseCommand):

    """Rebuild all projects command"""

    help = 'Import books from a csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            help='file path', required=False
        )

        parser.add_argument(
            '--json',
        help='json file path', required=False
        )

    def force_int(self, data):
        if data.isdigit():
            return int(data)

    def handle(self, *args, **options):
        file_path = options['csv']
        if file_path:
            with open(file_path, 'rt') as csvfile:
                spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',
                    quoting=csv.QUOTE_ALL, skipinitialspace=True)
                for row in spamreader:
                    title, author, editor, genre, language, year = row
                    if title == 'Título':
                        continue

                    g, __ = Genre.objects.get_or_create(
                        name=genre,
                        code=slugify(genre)
                    )
                    a, __ = Author.objects.get_or_create(
                        name=author
                    )
                    p, __ = Publisher.objects.get_or_create(
                        name=editor
                    )
                    b, __ = Book.objects.get_or_create(
                        title=title,
                        year_edition=int(year) if str.isdigit(year) else None,
                        genre=g,
                        publisher=p,
                        column=0,
                        number=0,

                    )
                    b.author.add(a)