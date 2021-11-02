from django.urls import path
from rest_framework import routers

from dashboard_app.auth import UserRegistrationView, LoginView, LogoutView
from dashboard_app.views import UserViewSet, PostViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('auth/register', UserRegistrationView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
