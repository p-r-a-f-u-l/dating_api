from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from customScript.validators import email_validation


class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_words):
        if not email:
            raise ValueError(_("Either Email is required."))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_words)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_words):
        if not email:
            raise ValueError(_("Either Email is required."))

        extra_words.setdefault("is_staff", True)
        extra_words.setdefault("is_superuser", True)
        extra_words.setdefault("is_admin", True)

        if extra_words.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_words.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_words)
        user.password = make_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    username = models.CharField(
        _("Username"), max_length=20, blank=True, null=True, unique=True
    )
    first_name = models.CharField(_("First Name"), max_length=20, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=20, blank=True, null=True)
    email = models.EmailField(
        _("Email"), validators=[email_validation], blank=True, unique=True
    )
    dob = models.DateField(blank=True, null=True)
    counter = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    profile_verified = models.BooleanField(default=False)
    device_id = models.CharField(max_length=60, null=True, blank=True)
    last_ip = models.GenericIPAddressField(
        _("Last Login IP Address"),
        protocol="IPv4",
        blank=True,
        null=True,
    )
    ua = models.CharField(_("User-Agent"), max_length=250, blank=True, editable=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def get_username(self):
        return f"{self.first_name}_{self.last_name}"

    def __str__(self) -> str:
        return self.email
