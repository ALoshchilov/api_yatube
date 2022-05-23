from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet, GroupViewSet, PostViewSet
)

API_VERSION = 'v1'
router_api_v1 = DefaultRouter()
routes = [
    (r'/groups', GroupViewSet, 'Group'),
    (r'/posts', PostViewSet, 'Post'),
    (r'/posts/(?P<post_id>\d+)/comments', CommentViewSet, 'Comment'),
]
for route in routes:
    url, viewset, basename = route
    router_api_v1.register(
        API_VERSION + url, viewset, basename
    )
urlpatterns = [
    path('', include(router_api_v1.urls)),
    path(API_VERSION + r'/api-token-auth/', views.obtain_auth_token),
]
