from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIGetToken, APISignup, UsersViewSet)

router_01 = DefaultRouter()

router_01.register('users', UsersViewSet, basename='user')

paths = [
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('', include(router_01.urls)),
    path('auth/signup/', APISignup.as_view(), name='signup'),
]
