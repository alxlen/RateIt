from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTitleSerializer,
                             PostTitleSerializer, ReviewSerializer,
                             TokenSerializer, UserRegistrationSerializer,
                             UserSerializer)
from api_yamdb.settings import EMAIL_SENDER
from reviews.models import Category, Genre, Review, Title, User


class UserRegisterAPIView(views.APIView):
    """Регистрация пользователя."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = self.generate_confirmation_code(user)
        self.send_confirmation_code(user.email, confirmation_code)

        return Response(
            {'email': serializer.data['email'],
             'username': serializer.data['username']},
            status=status.HTTP_200_OK
        )

    def generate_confirmation_code(self, user):
        return default_token_generator.make_token(user)

    def send_confirmation_code(self, email, confirmation_code):
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=EMAIL_SENDER,
            recipient_list=[email],
            fail_silently=False,
        )


class TokenValidationAPIView(views.APIView):
    """Класс токена."""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        access_token = AccessToken.for_user(user)
        token = {'token': str(access_token)}
        return Response(token, status=status.HTTP_200_OK)


class UserListViewSet(viewsets.ModelViewSet):
    """Профиль пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'delete', 'patch']
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_current_user_info.mapping.patch
    def update_current_user_info(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели жанра."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели произведения."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return PostTitleSerializer
        return GetTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ревью."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.get_title().id)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели коммента."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_review().id)
