from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("rec", views.LikeOrPassIndex, basename="dashboard")
router.register("likeV", views.UserLikeIndexView, basename="user dashboard")
router.register("passV", views.UserPassIndexView, basename="user dashboard")
router.register("superV", views.UserSuperLikeIndexView, basename="user dashboard")

urlpatterns = [
    path("people/<int:pk>/", views.LikeOrPassView.as_view()),
    path("", include(router.urls)),
]
