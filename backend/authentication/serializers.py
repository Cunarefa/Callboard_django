from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dashboard_app.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password',)

    def create(self, data):
        user = User(email=data['email'])
        user.set_password(data['password'])
        user.save()
        return user
