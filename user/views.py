from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from user.serializers import UserCreateSerializer, UserDetailSerializer, UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserManageView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class TokenCreateView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer
