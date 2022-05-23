from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import viewsets

from posts.models import Comment, Group, Post
from api.serializers import (
    CommentSerializer, GroupSerializer, PostSerializer
)

DELETE_DENIED_MESSAGE = 'Удаление чужого контента запрещено!'
EDIT_DENIED_MESSAGE = 'Изменение чужого контента запрещено!'
COMMENTS_NOT_FOUND_MESSAGE = 'Комментарии для поста ID {id} не найдены'
POST_NOT_FOUND_MESSAGE = 'Пост с ID {id} не найден'
POST_ID_KEY = 'post_id'


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id = self.kwargs.get(POST_ID_KEY)
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise NotFound(COMMENTS_NOT_FOUND_MESSAGE.format(id=id))
        return self.queryset.filter(post=post)

    def perform_create(self, serializer, **kwargs):
        id = self.kwargs.get(POST_ID_KEY)
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise NotFound(POST_NOT_FOUND_MESSAGE.format(id=id))
        serializer.save(
            author=self.request.user,
            post=post
        )

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied(EDIT_DENIED_MESSAGE)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, comment):
        if comment.author != self.request.user:
            raise PermissionDenied(DELETE_DENIED_MESSAGE)
        comment.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied(EDIT_DENIED_MESSAGE)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, post):
        if post.author != self.request.user:
            raise PermissionDenied(DELETE_DENIED_MESSAGE)
        post.delete()
