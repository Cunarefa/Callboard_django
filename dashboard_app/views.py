from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User, Post, Comment
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from .serializers import UserListSerializer, PostSerializer, CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsUserOrReadOnly]
    authentication_classes = [JWTAuthentication]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment(**serializer.validated_data, author=self.request.user, post_id=self.request.data['post_id'])
        if request.data.get('parent_id'):
            parent = Comment.objects.filter(id=request.data['parent_id']).first()
            parent.replies.add(comment, bulk=False)
            parent.save()
        comment.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(id=request.data['post_id']).first()

        post.likes.add(user)
        post.save()
        return Response('Like!', status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(id=request.data['post_id']).first()
        post.likes.remove(user)
        post.save()
        return Response('Unliked!', status.HTTP_200_OK)


class RepliesViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

