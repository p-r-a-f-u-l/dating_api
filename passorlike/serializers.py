from rest_framework import serializers
from .models import PassOrLikeModel, ProfileModel, UserConf
from userprofile.serializers import (
    DirectPicSerializer,
    MyInterestSerializer,
    MyZodiacSerializer,
    SexualOrientationSerializer,
    MyPetSerializer,
)


class UserConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConf
        fields = "__all__"


class UserSerializerShort(serializers.ModelSerializer):
    # dp = ImageSerializer(many=True)
    # interests = InterestSerializer(many=True)
    # lifestyle_zodioc = ZodiocSerializer()
    # sexual_orient = SexualOritSerializer()
    # pets_lover = PetSerializer()

    class Meta:
        model = ProfileModel
        fields = (
            "id",
            "userUID",
        )


class PassOrLikeSerializer(serializers.ModelSerializer):
    passProfile = UserSerializerShort(many=True)
    likeProfile = UserSerializerShort(many=True)
    superlikeProfile = UserSerializerShort(many=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    limitLess = serializers.SerializerMethodField()

    def get_limitLess(self, obj: PassOrLikeModel):
        request = self.context.get("request")
        user = UserConf.objects.filter(owner=request.user)
        serializer = UserConfSerializer(user, many=True)
        return serializer.data

    class Meta:
        model = PassOrLikeModel
        fields = (
            "id",
            "limitLess",
            "passProfile",
            "likeProfile",
            "superlikeProfile",
            "owner",
            "guid",
            "created_at",
            "updated_at",
            "limitLess",
        )
