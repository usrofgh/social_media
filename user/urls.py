from django.urls import path, include
from rest_framework import routers

from content.views import PostViewSet
from user.views import CreateUserView, TokenCreateView, UserViewSet, UserManageView

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", TokenCreateView.as_view(), name="login"),
    path("users/me/", UserManageView.as_view(), name="edit"),

    path("", include(router.urls))
]

app_name = "user"
