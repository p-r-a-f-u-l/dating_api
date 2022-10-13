from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("userprofile", views.UserProfileView, basename="setup profile")
router.register("pet", views.PetView)
router.register("direct", views.DirectView)
router.register("zodiac", views.ZodiacView)
router.register("sexual", views.SexualOrientView)
router.register("interest", views.InterestView)

urlpatterns = [
                  path("sexual/<int:pk>/", views.SexualOrientIndexView.as_view()),
                  path("interest/<int:pk>/", views.InterestIndexView.as_view()),
                  path("direct/<int:pk>/", views.DirectIndexView.as_view()),
                  path("zodiac/<int:pk>/", views.ZodiacIndexView.as_view()),
                  path("pet/<int:pk>/", views.PetIndexView.as_view()),
              ] + router.urls
