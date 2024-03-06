from rest_framework import viewsets

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet():
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet():
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
