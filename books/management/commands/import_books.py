from django.core.management.base import BaseCommand
from books.models import Author, Book, Genre, Publisher
import csv
import json
from pprint import pprint


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

    def handle(self, *args, **options):
        file_path = options['csv']
        json_path = options['json']
        if file_path:
            with open(file_path, 'rt') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    id = row[0]
                    title = row[1]
                    publisher = row[2]
                    genre = row[3]
        if json_path:
            json_data = open(json_path).read()
            data = json.loads(json_data)['objects']
            autori = data[0]['rows']
            for autore in autori:
                Author.objects.get_or_create(
                    id=autore[0],
                    name=autore[1],
                    last_name=autore[2]
                )
            editori = data[1]['rows']
            for editore in editori:
                Publisher.objects.get_or_create(
                    id=editore[0],
                    name=editore[1],
                )
            libri = data[2]['rows']
            for libro in libri:
                genre, _ = Genre.objects.get_or_create(
                    name=libro[3],
                    code=libro[3]
                )
                book, _ = Book.objects.get_or_create(
                    id=libro[0],
                    title=libro[1],
                    publisher_id=int(libro[2]),
                    genre=genre,
                    column=libro[4],
                    palco=libro[5],
                    number=libro[6],
                    year_edition=libro[7],
                    reprint_year=libro[8],
                    main_topic=libro[9],
                    secondary_topic=libro[10],
                    notes=libro[11]
                )
            pprint(data[3]['name'])
            libri_autori = data[3]['rows']
            for libro_autore in libri_autori:
                autore = Author.objects.get(pk=libro_autore[2])
                Book.objects.get(pk=libro_autore[1]).author.add(autore)
