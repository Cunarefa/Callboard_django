from django.urls import path
from rest_framework import routers

from .views import UserViewSet, PostViewSet, CommentViewSet, LikeView, RepliesViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('likes', LikeView.as_view(), name='like'),
    path('replies', RepliesViewSet.as_view(), name='reply'),
]

urlpatterns += router.urls
