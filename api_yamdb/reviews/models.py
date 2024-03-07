from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

TITLE_CUT = 25


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


class Review(models.Model):
    """Класс для отзыва+рейтинга."""

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
        return self.text[:30]


class Comment(models.Model):
    """Класс добавления комментария."""

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
        return self.text[:30]