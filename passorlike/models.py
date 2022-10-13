from django.db import models
from userprofile.models import ProfileModel
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()


class UserConf(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likesLimit = models.PositiveIntegerField(default=100)
    superlikeLimit = models.PositiveIntegerField(default=10)
    dislikeLimit = models.PositiveIntegerField(default=0)
    reloadLimit = models.PositiveIntegerField(default=10)
    boostLimit = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.owner)


class PassOrLikeModel(models.Model):
    guid = models.UUIDField(default=uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    limitLess = models.ForeignKey(UserConf, on_delete=models.CASCADE, default=None)
    passProfile = models.ManyToManyField(
        ProfileModel,
        related_name="pass_profile",
        blank=True,
    )
    likeProfile = models.ManyToManyField(
        ProfileModel,
        related_name="like_profile",
        blank=True,
        null=True,
    )
    superlikeProfile = models.ManyToManyField(
        ProfileModel,
        related_name="superlike_profile",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.guid)
