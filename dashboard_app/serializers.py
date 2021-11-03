from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dashboard_app.models import User, Post, Comment


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_staff', 'is_admin',)

    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    liked_posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_admin', 'posts', 'comments', 'liked_posts',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(read_only=True, source='author.id')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = UserListSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = '__all__'
