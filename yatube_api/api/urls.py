from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet, GroupViewSet, PostViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'api/v1/groups', GroupViewSet)
router.register(r'api/v1/posts', PostViewSet)
router.register(r'api/v1/posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register(r'api/v1/users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
