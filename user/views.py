from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from content.views import Pagination
from user.serializers import UserCreateSerializer, UserDetailSerializer, UserSerializer, AuthTokenSerializer, \
    UserListSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserManageView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    pagination_class = Pagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = self.request.query_params.get("username")
        email = self.request.query_params.get("email")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username=username)
        if email:
            queryset = queryset.filter(email=email)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action == "retrieve":
            return UserDetailSerializer

        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="toggle-following",
        permission_classes=[IsAuthenticated],
    )
    def toggle_following(self, request, pk=None):
        user = self.get_object()
        me = request.user
        if user == me:
            return Response({"status": "You can't follow yourself"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user not in me.followings.all():
            me.followings.add(user)
            return Response({"status": "following"}, status=status.HTTP_200_OK)
        else:
            me.followings.remove(user)
            return Response({"status": "unfollowing"}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": "Logged out"})


class TokenCreateView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer
