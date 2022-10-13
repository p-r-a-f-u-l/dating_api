from django.contrib import admin
from .models import MyPetModel, MyZodiacModel, SexualOrientationModel, ProfileModel, MyInterest, DirectPic

admin.site.register(MyPetModel)
admin.site.register(MyZodiacModel)
admin.site.register(SexualOrientationModel)
# admin.site.register(ProfileModel)
admin.site.register(MyInterest)
admin.site.register(DirectPic)


class ProfileModelAdmin(admin.ModelAdmin):
    model = ProfileModel
    list_display = (
        "id",
        "user",
        "userUID",
        "i_am",
        "userStatus",
        "verified",
        "ip_address",
    )
    search_fields = ("user",)
    list_filter = ("user",)

    def verified(self, obj):
        return obj.user.is_verified

    def ip_address(self, obj):
        return obj.user.last_ip


admin.site.register(ProfileModel, ProfileModelAdmin)
