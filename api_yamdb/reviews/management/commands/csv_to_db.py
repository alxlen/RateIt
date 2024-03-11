# import csv

# from django.core.management import BaseCommand

# from reviews.models import Title


# def import_data(file_path):
#     with open(file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             Title.objects.create(
#                 id=row['id'],
#                 name=row['name'],
#                 year=row['year'],
#                 category_id=row['category']
#             )


# if __name__ == '__main__':
#     csv_file_path = '/data/titles.csv'  # Replace with your actual file path
#     import_data(csv_file_path)


# CSV_FILES = [
#     ['users.csv', User],
#     ['titles.csv', Title],
#     ['category.csv', Category],
#     ['genre.csv', Genre],
#     ['genre_title.csv', GenreTitle],
#     ['review.csv', Review],
#     ['comments.csv', Comment],
# ]

# ALREDY_LOADED_ERROR_MESSAGE = """
# Если вам нужно перезагрузить дочерние данные из файла CSV,
# сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
# Затем запустите `python manage.py migrate` для новой пустой
# базы данных с таблицами"""


# class Command(BaseCommand):
#     help = "Загружает данные из файлов .csv"

#     def handle(self, *args, **options):

#         for file, model in CSV_FILES:
#         #     if model.objects.exists():
#         #         print(ALREDY_LOADED_ERROR_MESSAGE)
#         #         return
#         #     else:
#             with open('static/data/' + file, 'r', encoding='utf-8') as f:
#                 reader = csv.DictReader(f)
#                 for dict_row in reader:
#                     model.objects.get_or_create(**dict_row)

# class Command(BaseCommand):
#     # Show this when the user types help
#     help = "Загружает данные .csv"

#     def handle(self, *args, **options):

#         if User.objects.exists():
#             print('Данные users загружены.')
#             print(ALREDY_LOADED_ERROR_MESSAGE)
#             return

#         print("Загружаю users.")

#         for row in DictReader(open('./static/data/users.csv')):
#             user = User(id=row['id'], username=row['username'],
#                         email=row['email'], role=row['role'],
#                         bio=row['bio'], first_name=row['first_name'],
#                         last_name=row['last_name'])
#             user.save()


# class Command(BaseCommand):
#     # Show this when the user types help
#     help = "Загружает данные .csv"

#     def handle(self, *args, **options):

#         # if Title.objects.exists():
#         #     print('Данные titles загружены.')
#         #     print(ALREDY_LOADED_ERROR_MESSAGE)
#         #     return

#         print("Загружаю titles.")

#         for row in DictReader(open('./static/data/titles.csv')):
#             title = Title(id=row['id'], name=row['name'], year=row['year'],
#                           category_id=row['category'])
#             title.save()

