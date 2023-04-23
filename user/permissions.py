from rest_framework.permissions import BasePermission

from social_media_api.models import Post


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, post: Post):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return post.author == request.user
