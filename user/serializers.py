from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext as _


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username",
                  "first_name", "last_name",
                  "avatar", "bio", "is_staff", "password")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True, "min_length": 5,
                "style": {'input_type': 'password'}
            },
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username",
                  "first_name", "last_name",
                  "bio", "avatar",
                  "is_staff", "password")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5,
                         "style": {'input_type': 'password', }
                         },
        }


class UserListSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "followers_count", "followings_count")


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id", "email", "username",
            "first_name", "last_name",
            "bio", "avatar",
            "followings", "followers",
            "followers_count", "followings_count",
            "posts", "likes", "dislikes",
            "is_staff",)


class ToggleFollowingSerializer(serializers.Serializer):
    pass


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg)
        else:
            msg = _("Must include 'email' and 'password'")
            raise serializers.ValidationError(msg)

        attrs["user"] = user
        return attrs
