from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import (MAX_LENGTH_CATEGORY_GENRE,
                        MAX_LENGTH_CONFIRMATION_CODE,
                        MAX_LENGTH_EMAIL, MAX_LENGTH_ROLE, MAX_LENGTH_TITLE,
                        MAX_LENGTH_USERNAME, SCORE_VALIDATOR_MAX_VALUE,
                        SCORE_VALIDATOR_MIN_VALUE, TITLE_CUT,)
from .validators import validate_username, validate_year

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR), ]


class User(AbstractUser):
    """Класс пользователя."""

    username = models.CharField(
        validators=(validate_username,),
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )
    email = models.CharField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=MAX_LENGTH_ROLE,
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
        max_length=MAX_LENGTH_CONFIRMATION_CODE,
        null=True,
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
        return self.role == ADMIN or self.is_staff

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


class AddNameSlugFields(models.Model):
    """Абстрактная модель. Добавляет поле name и slug."""

    name = models.CharField('Название',
                            max_length=MAX_LENGTH_CATEGORY_GENRE)
    slug = models.SlugField('Идентификатор', unique=True,)

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name[:TITLE_CUT]


class Category(AddNameSlugFields):
    """Класс категория."""

    class Meta(AddNameSlugFields.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(AddNameSlugFields):
    """Класс жанр."""

    class Meta(AddNameSlugFields.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс произведение."""

    name = models.CharField('Название произведения',
                            max_length=MAX_LENGTH_TITLE)
    year = models.SmallIntegerField('Год выпуска', validators=[validate_year])
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
        default_related_name = 'titles'

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


class BaseReview(models.Model):
    """Абстрактный класс для отзыва и комментария."""

    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        """Возвращает текст отзыва/комментария."""
        return self.text[:TITLE_CUT]


class Review(BaseReview):
    """Класс отзыва и рейтинга."""

    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(
                SCORE_VALIDATOR_MIN_VALUE,
                message='Оценка не может быть ниже',
            ),
            MaxValueValidator(
                SCORE_VALIDATOR_MAX_VALUE,
                message='Оценка не может быть выше',
            ),
        ),
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review',
            ),
        )


class Comment(BaseReview):
    """Класс комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
