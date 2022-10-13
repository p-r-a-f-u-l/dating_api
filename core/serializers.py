from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User


class UsersSerializer(ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)

    def get_email(self, obj: User):
        request = self.context.get("request")
        return User.objects.get(id=request.user.id).email

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "dob"
        )
