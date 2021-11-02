from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from dashboard_app.models import User
from dashboard_app.serializers import UserSerializer, RefreshTokenSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': user.email,
                'token': str(refresh.access_token),
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('The password is incorrect!')

        token = RefreshToken.for_user(user)
        update_last_login(None, user)

        return Response({'user': user.email, 'token': str(token.access_token)})



