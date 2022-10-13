from rest_framework.routers import SimpleRouter
from django.urls import path, include
from . import views


urlpatterns = [
    path("user/", views.UserCreateIndex.as_view(), name="create_user"),
    path("user/me/", views.UserMeIndex.as_view(), name="user_me"),
    path("user/<emailID>/", views.LoginIndex.as_view(), name="login_user"),
    # path("", include(router.urls)),
]
