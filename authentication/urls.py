from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserRegistrationView, LoginView, LogoutView

router = DefaultRouter()
router.register('register', UserRegistrationView, basename='register')

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
