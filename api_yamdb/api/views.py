from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api_yamdb.api.serializers import ReviewSerializer, CommentSerializer
from api_yamdb.reviews.models import Title, Review, Comment


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ревью."""

    serializer_class = ReviewSerializer
    permission_classes = (
        # тут пермишены
        # IsAuthenticatedOrReadOnly,
        # IsAuthorModeratorAdminOrReadOnly,
    )

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели коммента."""

    serializer_class = CommentSerializer
    permission_classes = (
        # тут пермишены
        # IsAuthenticatedOrReadOnly,
        # IsAuthorModeratorAdminOrReadOnly,
    )

    def perform_create(self, serializer):
        """Создание нового коммента."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        """Получение кверисета."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)
