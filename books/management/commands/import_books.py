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
            '--genre',
            help='Genre', required=False
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
        genre_arg = options['genre']
        if file_path:
            with open(file_path, 'rt') as csvfile:
                spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',
                    quoting=csv.QUOTE_ALL, skipinitialspace=True)
                for row in spamreader:
                    try:
                        title, author, editor, genre, language, year = row
                        if title == 'Título':
                            continue
                        if genre_arg:
                            genre = genre_arg
                        genre = genre.strip()
                        g, __ = Genre.objects.get_or_create(
                            name=genre, code=genre)
                        a, __ = Author.objects.get_or_create(
                            name=author
                        )
                        p = Publisher.objects.filter(
                            name=editor
                        )
                        if p:
                            p = p[0]
                        else:
                            p = Publisher.objects.create(
                                name=editor)
                        b, __ = Book.objects.get_or_create(
                            title=title,
                            year_edition=int(year) if str.isdigit(year) else None,
                            genre=g,
                            publisher=p,
                            column=0,
                            number=0,

                        )
                        b.author.add(a)
                    except Exception as e:
                        print('ERRORE ({}): {}'.format(e ,title))