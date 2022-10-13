import uuid

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.validators import ValidationError
from django.utils.translation import gettext_lazy as _

iam = {
    ("Women", "Women"),
    ("Men", "Men"),
    ("Other", "Other")
}

user_Status = {
    ("basic", "basic"),
    ("premium", "premium"),
    ("super", "super")
}

User = get_user_model()


class SexualOrientationModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(User, blank=True, null=True)
    sexual_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sexual_name


class MyInterest(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(User, blank=True, null=True)
    interest_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.interest_name


class DirectPic(models.Model):
    image_click = models.ImageField(upload_to="media/dp")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class MyZodiacModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(User, blank=True, null=True)
    horo_sign = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.horo_sign


class MyPetModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(User, blank=True, null=True)
    pet_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pet_name


class ProfileModel(models.Model):
    userUID = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    i_am = models.CharField(max_length=10, choices=iam, default="Men")
    show_gender = models.BooleanField(default=True)
    sexual_orient = models.ManyToManyField(SexualOrientationModel, blank=True, null=True)
    show_orient = models.BooleanField(default=False)
    show_me = models.CharField(max_length=10, choices=iam, default="Women")
    my_graduation = models.CharField(max_length=280, blank=True, null=True)
    my_interest = models.ManyToManyField(MyInterest, blank=True, null=True)
    dp_image = models.ManyToManyField(DirectPic, blank=True, null=True)
    smart_photo = models.BooleanField(default=True)
    about_me = models.TextField(max_length=1000, blank=True, null=True)
    zodiac = models.OneToOneField(MyZodiacModel, blank=True, null=True, on_delete=models.CASCADE)
    pets = models.OneToOneField(MyPetModel, blank=True, null=True, on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=360, blank=True, null=True)
    livingIn = models.CharField(max_length=120, blank=True, null=True)
    show_myAge = models.BooleanField(default=True)
    show_myDistance = models.BooleanField(default=True)
    userStatus = models.CharField(choices=user_Status, max_length=12, default="basic")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.userUID)

    # def clean(self):
    #     sexual = self.sexual_orient
    #     if sexual.count() > 4:
    #         raise ValidationError(detail="Error", code=404)
