from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                       GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

router_01 = DefaultRouter()


router_01.register('categories', CategoryViewSet, basename='category')
router_01.register('genres', GenreViewSet, basename='genre')
router_01.register('titles', TitleViewSet, basename='titles')
router_01.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_01.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_01.register('users', UsersViewSet, basename='user')

paths = [
    path('auth/signup/', APISignup.as_view(), name='signup'),
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('', include(router_01.urls)),
]


urlpatterns = [
    path('v1/', include(paths))
]
