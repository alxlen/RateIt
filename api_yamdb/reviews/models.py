from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]

TITLE_CUT = 25


class User(AbstractUser):
    """Класс пользователя."""

    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        null=False,
    )
    email = models.CharField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )

    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class Category(models.Model):
    """Класс категория."""

    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True,
                            validators=[])

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TITLE_CUT]


class Genre(models.Model):
    """Класс жанр."""

    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True,
                            validators=[])

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TITLE_CUT]


class Title(models.Model):
    """Класс произведение."""

    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField(
        'Год выпуска',
        validators=[
            MinValueValidator(0,
                              message='Значение года должно быть больше 0.'),
            MaxValueValidator(datetime.now().year,
                              message='Произведение еще не создано.')
        ],

    )
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='titles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TITLE_CUT]


class GenreTitle(models.Model):
    """Класс связи произведения с жанрами."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Жанр')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} относится к {self.genre}'
