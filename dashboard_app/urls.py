from django.urls import path
from rest_framework import routers

from dashboard_app.auth import UserRegistrationView, LoginView, LogoutView
from dashboard_app.views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
