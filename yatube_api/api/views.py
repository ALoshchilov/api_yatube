from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status, viewsets

from posts.models import Comment, Group, Post, User
from api.serializers import (
    CommentSerializer, GroupSerializer, PostSerializer, UserSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(id=self.kwargs.get('post_id'))
        )

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def destroy(self, request, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def destroy(self, request, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
