import csv

from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


CSV_FILES_MODELS = [
    ['users.csv', User],
    ['category.csv', Category],
    ['genre.csv', Genre],
    ['titles.csv', Title],
    ['genre_title.csv', GenreTitle],
    ['review.csv', Review],
    ['comments.csv', Comment],
]


PUL = ('title', 'category', 'author')


def qq(key):
    return f'{key}_id' if key in PUL else key


def ww(key, value):
    return int(value) if key in PUL or 'id' in key else value


class Command(BaseCommand):
    help = 'Загружает данные из файлов .csv'

    def handle(self, *args, **options):

        self.stdout.write(self.style.NOTICE('Очистка базы данных'))

        for _, model in reversed(CSV_FILES_MODELS):
            model.objects.all().delete()

        self.stdout.write(self.style.NOTICE('Загрузка данных'))

        for file, model in CSV_FILES_MODELS:
            with open('static/data/' + file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                model.objects.bulk_create([model(
                    **{qq(key): ww(key, value) for key, value in row.items()}
                ) for row in reader])

        self.stdout.write(self.style.SUCCESS('Импорт завершен'))
