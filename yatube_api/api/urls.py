from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet, GroupViewSet, PostViewSet
)

API_VERSION = 'v1/'
router_api_v1 = DefaultRouter()
router_api_v1.register(r'groups', GroupViewSet, 'Group')
router_api_v1.register(r'posts', PostViewSet, 'Post')
router_api_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, 'Comment'
)
urlpatterns = [
    path(API_VERSION, include(router_api_v1.urls)),
    path(API_VERSION + r'api-token-auth/', views.obtain_auth_token),
]
