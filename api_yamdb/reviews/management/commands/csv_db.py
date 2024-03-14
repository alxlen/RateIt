import csv

from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

DATA_EXISTS_ERROR = """
ВНИМАНИЕ! База данных не пустая.
Для перезаписи данных из файлов CSV:
1) удалите файл db.sqlite3;
2) выполните `python manage.py migrate` для создания пустой базы данных;
3) выполните скрипт `python manage.py csv_db` для заполнения базы данных.
"""


def import_category():
    if Category.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/category.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )


def import_genre():
    if Genre.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/genre.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )


def import_titles():
    if Title.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/titles.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )


def import_genre_title():
    if GenreTitle.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/genre_title.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    genre_id=row['genre_id'],
                    title_id=row['title_id'],
                )


def import_users():
    if User.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/users.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )


def import_reviews():
    if Review.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/review.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )


def import_comments():
    if Comment.objects.exists():
        print(DATA_EXISTS_ERROR)
        return
    else:
        with open('./static/data/comments.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    text=row['text'],
                    pub_date=row['pub_date'],
                    author_id=row['author'],
                    review_id=row['review_id'],
                )


class Command(BaseCommand):
    help = "Загружает данные из файлов .csv"

    def handle(self, *args, **options):
        import_category()
        import_genre()
        import_titles()
        import_genre_title()
        import_users()
        import_reviews()
        import_comments()
        self.stdout.write(self.style.SUCCESS('Операция завершена.'))


# CSV_FILES_MODELS_FIELDS = [
#     ['users.csv', User, (None)],
#     ['category.csv', Category, (None)],
#     ['genre.csv', Genre, (None)],
#     ['titles.csv', Title, ("id", "name", "year", "category_id")],
#    # ['genre_title.csv', GenreTitle, (None)],
#    # ['review.csv', Review],
#    # ['comments.csv', Comment],
# ]


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
#                 for row in reader:
#                     model.objects.get_or_create(**row)

#         self.stdout.write(self.style.SUCCESS('Импорт завершен'))
