from rest_framework import serializers

from posts.models import Comment, Group, Post, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    # id = 0
    # def is_named_bar(self, foo):
    #     self.custom_id = self.custom_id + 1
    #     return self.custom_id
    # order_number = serializers.SerializerMethodField('is_named_bar')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created', 'author', 'post',)
        read_only_fields = ('id', 'created', 'post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date',)
        read_only_fields = ('id', 'pub_date', 'author',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email',
            'date_joined', 'groups',
        )
        read_only_fields = (
            'id', 'date_joined',
        )
