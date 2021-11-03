from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard_app.models import User, Post, Comment
from dashboard_app.permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from dashboard_app.serializers import UserListSerializer, PostSerializer, CommentSerializer, LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser | IsUserOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def partial_update(self, request, partial=True, *args, **kwargs):
        self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            User.objects.filter(id=kwargs['pk']).update(**serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, partial=True, *args, **kwargs):
        self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            Post.objects.filter(id=kwargs['pk']).update(**serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.request.data['post_id'])


class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = [LikeSerializer]

    def create(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(id=request.data['post_id']).first()

        post.likes.add(user)
        post.save()
        return Response('Like!')

    def delete(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(id=request.data['post_id']).first()
        post.likes.remove(user)
        post.save()
        return Response('Unliked!')













