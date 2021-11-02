from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dashboard_app.models import User, Post


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email',)


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = LikesSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'



