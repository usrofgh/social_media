from django.db import transaction
from rest_framework import serializers

from content.models import Post, Tag, Comment


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post_id", "created_at", "text")


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "tag_name")


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Post
        fields = (
            "id", "text", "tags",
            "author", "created_at",
            "likes_count", "dislikes_count",
            "likes", "dislikes",
            "comments_count", "comments"
        )
        read_only_fields = (
            "id", "author", "created_at",
            "likes_count", "dislikes_count",
            "likes", "dislikes",
            "comments_count"
        )

    @transaction.atomic
    def create(self, validated_data):
        tag_names = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(tag_name=tag_name)
            post.tags.add(tag)
        return post

    def update(self, instance: Post, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.tags = validated_data.get("tags", instance.tags)
        instance.save()
        return instance


class PostListSerializer(PostSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="tag_name",
    )

    class Meta:
        model = Post
        fields = (
            "id", "author",
            "likes_count", "dislikes_count",
            "comments_count", "text", "tags"
        )


class PostDetailSerializer(PostSerializer):
    pass
