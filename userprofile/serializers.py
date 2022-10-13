from rest_framework import serializers

from .models import MyPetModel, MyZodiacModel, SexualOrientationModel, MyInterest, DirectPic, ProfileModel


class SexualOrientationSerializer(serializers.ModelSerializer):
    isSelected = serializers.SerializerMethodField()

    def get_isSelected(self, sexualOrientationModel):
        request = self.context.get("request")
        if sexualOrientationModel.user.filter(id=request.user.id).exists():
            return True
        return False

    class Meta:
        model = SexualOrientationModel
        fields = (
            "id",
            "guid",
            "sexual_name",
            "isSelected",
            "created_at",
            "updated_at",
        )


class MyInterestSerializer(serializers.ModelSerializer):
    isSelected = serializers.SerializerMethodField()

    def get_isSelected(self, myInterest):
        request = self.context.get("request")
        if myInterest.user.filter(id=request.user.id).exists():
            return True
        return False

    class Meta:
        model = MyInterest
        fields = (
            "id",
            "guid",
            "interest_name",
            "isSelected",
            "created_at",
            "updated_at",
        )


class DirectPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectPic
        fields = "__all__"


class MyZodiacSerializer(serializers.ModelSerializer):
    isSelected = serializers.SerializerMethodField()

    def get_isSelected(self, myZodiacModel):
        request = self.context.get("request")
        if myZodiacModel.user.filter(id=request.user.id).exists():
            return True
        return False

    class Meta:
        model = MyZodiacModel
        fields = (
            "id",
            "guid",
            "horo_sign",
            "isSelected",
            "created_at",
            "updated_at",
        )


class MyPetSerializer(serializers.ModelSerializer):
    isSelected = serializers.SerializerMethodField()

    def get_isSelected(self, myPetModel):
        request = self.context.get("request")
        if myPetModel.user.filter(id=request.user.id).exists():
            return True
        return False

    class Meta:
        model = MyPetModel
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    # user = serializers.SerializerMethodField()
    #
    # def get_user(self, obj: ProfileModel):
    #     request = self.context.get("request")
    #     return ProfileModel.objects.get(user=request.user.id).user.id

    class Meta:
        model = ProfileModel
        fields = "__all__"
