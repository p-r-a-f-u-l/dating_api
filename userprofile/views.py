from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status, validators

from .serializers import SexualOrientationSerializer, DirectPicSerializer, ProfileSerializer, MyInterestSerializer, \
    MyPetSerializer, MyZodiacSerializer
from .models import MyPetModel, MyZodiacModel, SexualOrientationModel, MyInterest, DirectPic, ProfileModel
from django.shortcuts import get_object_or_404

# custom Script Import
from customScript.customResponse import ResponseInfo

from passorlike.models import PassOrLikeModel, UserConf


class UserProfileView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UserProfileView, self).__init__(**kwargs)

    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    lookup_field = "id"
    pagination_class = None

    def get_queryset(self):
        return ProfileModel.objects.filter(user=self.request.user.id)

    def get_serializer_context(self):
        context = super(UserProfileView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        if not UserConf.objects.filter(owner=self.request.user).exists():
            user_conf = UserConf.objects.create(owner=self.request.user)
            PassOrLikeModel.objects.create(owner=self.request.user, limitLess=user_conf)
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response_data = super(UserProfileView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "No Data Found."
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class PetView(ModelViewSet):
    queryset = MyPetModel.objects.all()
    serializer_class = MyPetSerializer
    permission_class = None


class PetIndexView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(MyPetModel, id=pk)
        serializer = MyPetSerializer(query, context={"request": self.request})
        context = {
            "message": "success",
            "error": None,
            "data": serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, pk):
        query = get_object_or_404(MyPetModel, id=pk)
        if not MyPetModel.objects.all().filter(user=self.request.user).exists():
            query.user.add(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Added."
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Already Added."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = get_object_or_404(MyPetModel, id=pk)
        if query.user.filter(id=self.request.user.id).exists():
            query.user.remove(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Removed."
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Not Exists."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class ZodiacView(ModelViewSet):
    queryset = MyZodiacModel.objects.all()
    serializer_class = MyZodiacSerializer
    permission_class = None
    http_method_names = ('get',)


class ZodiacIndexView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(MyZodiacModel, id=pk)
        serializer = MyZodiacSerializer(query, context={"request": self.request})
        context = {
            "message": "success",
            "error": None,
            "data": serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, pk):
        query = get_object_or_404(MyZodiacModel, id=pk)
        if not MyZodiacModel.objects.all().filter(user=self.request.user).exists():
            query.user.add(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Added."
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Already Added."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = get_object_or_404(MyZodiacModel, id=pk)
        if query.user.filter(id=self.request.user.id).exists():
            query.user.remove(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Removed."
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Not Exists."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class SexualOrientView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SexualOrientView, self).__init__(**kwargs)

    queryset = SexualOrientationModel.objects.all()
    serializer_class = SexualOrientationSerializer
    http_method_names = ("get",)
    pagination_class = None

    def get_serializer_context(self):
        context = super(SexualOrientView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        response_data = super(SexualOrientView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "No Data Found."
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class SexualOrientIndexView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(SexualOrientationModel, id=pk)
        serializer = SexualOrientationSerializer(query, context={"request": self.request})
        context = {
            "message": "success",
            "error": None,
            "data": serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, pk):
        query = get_object_or_404(SexualOrientationModel, id=pk)
        if not query.user.filter(id=self.request.user.id).exists():
            query.user.add(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Added."
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Already Added."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = get_object_or_404(SexualOrientationModel, id=pk)
        if query.user.filter(id=self.request.user.id).exists():
            query.user.remove(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Removed."
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Not Exists."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class InterestView(ModelViewSet):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(InterestView, self).__init__(**kwargs)

    queryset = MyInterest.objects.all()
    serializer_class = MyInterestSerializer
    pagination_class = None
    http_method_names = ('get',)

    def list(self, request, *args, **kwargs):
        response_data = super(InterestView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "No Data Found."
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class InterestIndexView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(MyInterest, id=pk)
        serializer = MyInterestSerializer(query, context={"request": self.request})
        context = {
            "message": "success",
            "error": None,
            "data": serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, pk):
        query = get_object_or_404(MyInterest, id=pk)
        if not query.user.filter(user=self.request.user).exists():
            query.user.add(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Added."
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Already Added."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = get_object_or_404(MyInterest, id=pk)
        if query.user.filter(id=self.request.user.id).exists():
            query.user.remove(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Removed."
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Not Exists."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class DirectView(ModelViewSet):
    queryset = DirectPic.objects.all()
    serializer_class = DirectPicSerializer
    permission_class = None
    http_method_names = ('get',)


class DirectIndexView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(DirectPic, id=pk)
        serializer = DirectPicSerializer(query, context={"request": self.request})
        context = {
            "message": "success",
            "error": None,
            "data": serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, pk):
        query = get_object_or_404(DirectPic, id=pk)
        if not query.user.filter(id=self.request.user.id).exists():
            query.user.add(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Added."
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Already Added."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = get_object_or_404(DirectPic, id=pk)
        if query.user.filter(id=self.request.user.id).exists():
            query.user.remove(self.request.user)
            context = {
                "message": "success",
                "error": None,
                "data": "Removed."
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "Not Exists."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
