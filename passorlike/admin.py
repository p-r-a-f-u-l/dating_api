from django.contrib import admin
from .models import PassOrLikeModel, UserConf

admin.site.register(PassOrLikeModel)
# admin.site.register(ProfileModel)
admin.site.register(UserConf)
