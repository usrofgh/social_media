from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from content.models import Post
from content.serializers import (
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
)
from user.permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related("tags", "likes", "dislikes", "comments")
    serializer_class = PostSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        tags = self.request.query_params.get("tags")
        author = self.request.query_params.get("author")
        queryset = self.queryset

        if tags:
            tags = tags.split(",")
            for tag in tags:
                queryset = queryset.filter(tags__tag_name=tag)

        if author:
            queryset = queryset.filter(author__username=author)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def like(self, request, pk=None):
        me = self.request.user
        post = self.get_object()
        if me in post.likes.all():
            post.likes.remove(me)
            return Response({"status": "undo like"})

        if me in post.dislikes.all():
            post.dislikes.remove(me)

        post.likes.add(me)
        return Response({"status": "like"})

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def dislike(self, request, pk=None):
        me = self.request.user
        post = self.get_object()
        if me in post.dislikes.all():
            post.dislikes.remove(me)
            return Response({"status": "undo dislike"})

        if me in post.likes.all():
            post.likes.remove(me)

        post.dislikes.add(me)
        return Response({"status": "dislike"})
