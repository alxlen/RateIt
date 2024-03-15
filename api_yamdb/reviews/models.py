from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constans import (MAX_LENGTH_CONFIRMATION_CODE, MAX_LENGTH_EMAIL,
                       MAX_LENGTH_ROLE, MAX_LENGTH_USERNAME,)
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
        max_length=MAX_LENGHT_USERNAME,
        unique=True,
        null=False,
    )
    email = models.CharField(
        max_length=MAX_LENGHT_EMAIL,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        'роль',
        max_length=MAX_LENGHT_ROLE,
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
        max_length=MAX_LENGHT_CONFIRMATION_CODE,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


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
    slug = models.SlugField(
        'Идентификатор',
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(regex='^[-a-zA-Z0-9_]+$',
                           message='Недопустимый символ в названии.'),
        ]
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TITLE_CUT]


class Genre(models.Model):
    """Класс жанр."""

    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(
        'Идентификатор',
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(regex='^[-a-zA-Z0-9_]+$',
                           message='Недопустимый символ в названии.'),
        ]
    )

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


class Review(models.Model):
    """Класс отзыва и рейтинга."""

    text = models.TextField(verbose_name='текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(
                1,
                message='Оценка не может быть ниже',
            ),
            MaxValueValidator(
                10,
                message='Оценка не может быть выше',
            ),
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review',
            ),
        )

    def __str__(self):
        """Возвращает текст отзыва."""
        return self.text[:TITLE_CUT]


class Comment(models.Model):
    """Класс комментария."""

    text = models.TextField(verbose_name='текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        """Возвращает текст комментария."""
        return self.text[:TITLE_CUT]
