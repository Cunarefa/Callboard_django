from rest_framework import serializers
from .models import User, Post, Comment


class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(read_only=True, source='author.id')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    my_absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    post = serializers.ReadOnlyField(source='post.id')
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'replies', 'post', 'parent')








