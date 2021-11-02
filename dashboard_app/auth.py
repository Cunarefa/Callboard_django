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
from dashboard_app.serializers import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': user.email,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
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

        return Response({'user': user.email, 'access': str(token.access_token), 'refresh': str(token)})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response("Successful Logout", status=status.HTTP_200_OK)
        except Exception as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
