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


def extract_data():
    for file, model in CSV_FILES_MODELS:
        with open('static/data/' + file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if model == User:
                for row in reader:
                    model.objects.create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
            elif model == Category:
                for row in reader:
                    model.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
            elif model == Genre:
                for row in reader:
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
            elif model == Title:
                for row in reader:
                    model.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category'],
                    )
            elif model == GenreTitle:
                for row in reader:
                    model.objects.create(
                        id=row['id'],
                        genre_id=row['genre_id'],
                        title_id=row['title_id'],
                    )
            elif model == Review:
                for row in reader:
                    model.objects.create(
                        id=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
            else:
                # model == Comment
                for row in reader:
                    model.objects.create(
                        id=row['id'],
                        text=row['text'],
                        pub_date=row['pub_date'],
                        author_id=row['author'],
                        review_id=row['review_id'],
                    )


class Command(BaseCommand):
    help = 'Загружает данные из файлов .csv'

    def handle(self, *args, **options):

        self.stdout.write(self.style.NOTICE('Очистка базы данных'))

        for _, model in reversed(CSV_FILES_MODELS):
            model.objects.all().delete()

        self.stdout.write(self.style.NOTICE('Зарузка данных'))

        extract_data()

        self.stdout.write(self.style.SUCCESS('Операция завершена.'))

# психанул)
# CSV_FILES_MODELS_FIELDS = [
#     ['users.csv', User, (None)],
#     ['category.csv', Category, (None)],
#     ['genre.csv', Genre, (None)],
#     ['titles.csv', Title, ("id", "name", "year", "category_id")],
#     ['genre_title.csv', GenreTitle, (None)],
#     ['review.csv', Review],
#     ['comments.csv', Comment],
# ]


# PUL = ('category_id', 'author_id')


# def ww(key, value):
#     return int(value) if key in PUL else value

# def qq(key):
#     return


# class Command(BaseCommand):
#     help = 'Загружает данные из файлов .csv'

#     def handle(self, *args, **options):

#         self.stdout.write(self.style.NOTICE('Очистка базы данных'))

#         for _, model, _ in reversed(CSV_FILES_MODELS_FIELDS):
#             model.objects.all().delete()

#         self.stdout.write(self.style.NOTICE('Загрузка данных'))

#         for file, model, field_names in CSV_FILES_MODELS_FIELDS:
#             with open('static/data/' + file, 'r', encoding='utf-8') as f:
#                 reader = csv.DictReader(f, fieldnames=field_names)
#                 for row in islice(reader, 0, None):
#                     new_dict = {
#                         key: ww(key, value) for key, value in row.items()
#                     }
#                     model.objects.get_or_create(**new_dict)

#         self.stdout.write(self.style.SUCCESS('Импорт завершен'))
