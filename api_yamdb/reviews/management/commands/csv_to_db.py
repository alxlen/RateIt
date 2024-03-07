import csv

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

CSV_FILES = [
    ['category.csv', Category],
    ['comments.csv', Comment],
    ['genre_title.csv', GenreTitle],
    ['genre.csv', Genre],
    ['review.csv', Review],
    ['titles.csv', Title],
    ['users.csv', User],
]

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить дочерние данные из файла CSV,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загружает данные из файлов .csv"

    def handle(self, *args, **options):

        for file, model in CSV_FILES:
            if model.objects.exists():
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return
            else:
                with open('static/data/' + file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for dict_row in reader:
                        model.objects.get_or_create(**dict_row)
