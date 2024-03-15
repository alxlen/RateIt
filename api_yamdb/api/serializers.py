from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'role', 'bio'
        )


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""

    email = serializers.EmailField(max_length=254, required=True,)
    username = serializers.CharField(
        max_length=150, required=True,
        validators=[UnicodeUsernameValidator(), validate_username]
    )

    def create(self, validated_data):
        try:
            user, created = User.objects.get_or_create(**validated_data)
            return user
        except IntegrityError:
            raise serializers.ValidationError(
                "Неуникальный username или email."
            )


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанра."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведения при GET запросах."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class PostTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведения при POST запросах."""

    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         allow_empty=True, required=True,
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, title):
        "Метод для вывода результата запроса."
        serializer = GetTitleSerializer(title)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ревью."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение',
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
