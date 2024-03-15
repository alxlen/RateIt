from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, TokenValidationAPIView,
                    UserListViewSet, UserRegisterAPIView)

router_01 = DefaultRouter()


router_01.register('categories', CategoryViewSet, basename='category')
router_01.register('genres', GenreViewSet, basename='genre')
router_01.register('titles', TitleViewSet, basename='titles')
router_01.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_01.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_01.register('users', UserListViewSet, basename='user')


auth_urls = [
    path('signup/', UserRegisterAPIView.as_view(), name='signup'),
    path('token/', TokenValidationAPIView.as_view(), name='get_token'),
]

paths = [
    path('auth/', include(auth_urls)),
    path('', include(router_01.urls)),
]


urlpatterns = [
    path('v1/', include(paths))
]
