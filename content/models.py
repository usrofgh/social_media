from django.db import models


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(
        to="Post",
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = "comments"

    def __str__(self):
        return f"Post id: {self.post.id}, Author id: {self.author.id}, created: {self.created_at}"


class Tag(models.Model):
    tag_name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self) -> str:
        return self.tag_name


class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(to=Tag, related_name="posts")
    author = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
        related_name="posts"
    )

    likes = models.ManyToManyField(
        to="user.User",
        related_name="likes",
    )

    dislikes = models.ManyToManyField(
        to="user.User",
        related_name="dislikes",
    )

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def dislikes_count(self) -> int:
        return self.dislikes.count()

    @property
    def comments_count(self) -> int:
        return self.comments.count()

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"Post id: {self.id}"
