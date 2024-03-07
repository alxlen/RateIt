from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router_01 = DefaultRouter()


router_01.register('categories', CategoryViewSet, basename='category')
router_01.register('genres', GenreViewSet, basename='genre')
router_01.register('titles', TitleViewSet, basename='titles')


paths = [
    path('', include(router_01.urls)),
    #  пути авторизации
]


urlpatterns = [
    path('v1/', include(paths))
]
