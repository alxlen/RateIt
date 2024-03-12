import csv

from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

# CSV_FILES = [
#     ['category.csv', Category],
#     ['comments.csv', Comment],
#     ['genre_title.csv', GenreTitle],
#     ['genre.csv', Genre],
#     ['review.csv', Review],
#     ['titles.csv', Title],
#     ['users.csv', User],
# ]

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
                Category.objects.create(
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
                    description=row['description'],
                    category_id=['category'],
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
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                    author_id=['author'],
                    title_id=['title_id'],
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
                    author_id=['author'],
                    review_id=['review_id'],
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
                    title_id=['title_id'],
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
                    bio=['bio'],
                    first_name=['first_name'],
                    last_name=['last_name']
                )


class Command(BaseCommand):
    help = "Загружает данные из файлов .csv"

    def handle(self, *args, **options):
        # for file, model in CSV_FILES:
        #     if model.objects.exists():
        #         print(DATA_EXISTS_ERROR)
        #         return
        #     else:
        import_category()
        import_genre()
        import_titles()
        import_reviews()
        import_comments()
        import_genre_title()
        import_users()
        self.stdout.write(self.style.SUCCESS('Данные импортированы.'))


                # with open('static/data/' + file, 'r', encoding='utf-8') as f:
                #     reader = csv.DictReader(f)
                #     for dict_row in reader:
                #         model.objects.get_or_create(**dict_row)
