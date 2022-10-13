from rest_framework.viewsets import ModelViewSet

from userprofile.models import ProfileModel
from .models import PassOrLikeModel, UserConf
from .serializers import PassOrLikeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from customScript.customResponse import ResponseInfo


class LikeOrPassIndex(ModelViewSet):
    queryset = PassOrLikeModel.objects.all()
    serializer_class = PassOrLikeSerializer
    http_method_names = ("get",)

    def get_queryset(self):
        user = PassOrLikeModel.objects.exclude(owner=self.request.user)
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class UserLikeIndexView(ModelViewSet):
    queryset = PassOrLikeModel.objects.filter(likeProfile__gt=0)
    serializer_class = PassOrLikeSerializer
    http_method_names = ("get",)

    def get_queryset(self):
        user = PassOrLikeModel.objects.exclude(owner=self.request.user)
        return user


class UserPassIndexView(ModelViewSet):
    queryset = PassOrLikeModel.objects.filter(passProfile__gt=0)
    serializer_class = PassOrLikeSerializer
    http_method_names = ("get",)

    def get_queryset(self):
        user = PassOrLikeModel.objects.exclude(owner=self.request.user)
        return user


class UserSuperLikeIndexView(ModelViewSet):
    queryset = PassOrLikeModel.objects.filter(superlikeProfile__gt=0)
    serializer_class = PassOrLikeSerializer
    http_method_names = ("get",)

    def get_queryset(self):
        user = PassOrLikeModel.objects.exclude(owner=self.request.user)
        return user


class LikeOrPassView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(PassOrLikeModel, id=pk)
        serializer = PassOrLikeSerializer(query, context={"request": request})
        return Response(data=serializer.data)

    def post(self, request, pk):
        querysets = UserConf.objects.filter(owner=self.request.user).first()
        query = get_object_or_404(PassOrLikeModel, id=pk)
        additem = get_object_or_404(ProfileModel, user_id=self.request.user.id)
        if (
                not query.passProfile.filter(user=request.user.id).exists()
                and not query.likeProfile.filter(user=request.user.id).exists()
                and not query.superlikeProfile.filter(user=request.user.id).exists()
        ):
            query.likeProfile.add(additem)
            count = querysets.likesLimit
            count -= 1
            UserConf.objects.update(likesLimit=abs(count))
        else:
            return Response(data={"data": "Already"})
        return Response(data={"data": "data"})

    def delete(self, request, pk):
        query = get_object_or_404(PassOrLikeModel, id=pk)
        additem = get_object_or_404(ProfileModel, user_id=self.request.user.id)
        if (
                not query.passProfile.filter(user=request.user.id).exists()
                and not query.likeProfile.filter(user=request.user.id).exists()
                and not query.superlikeProfile.filter(user=request.user.id).exists()
        ):
            query.passProfile.add(additem)
        else:
            return Response(data={"data": "Already"})
        return Response(data={"data": "data"})

    def patch(self, request, pk):
        # querysets = get_object_or_404(UserConf, owner=)
        querysets = UserConf.objects.filter(owner=self.request.user).first()
        additem = get_object_or_404(ProfileModel, user_id=self.request.user.id)
        query = get_object_or_404(PassOrLikeModel, id=pk)
        if (
                not query.passProfile.filter(user=request.user.id).exists()
                and not query.likeProfile.filter(user=request.user.id).exists()
                and not query.superlikeProfile.filter(user=request.user.id).exists()
        ):
            query.superlikeProfile.add(additem)
            count = querysets.superlikeLimit
            count -= 1
            UserConf.objects.update(superlikeLimit=abs(count))
        else:
            return Response(data={"data": "Already"})
        return Response(data={"data": 100})


class ReloadViewIndex(APIView):
    def get(self, request):
        pass


class AddBoostIndex(APIView):
    def get(self, request):
        pass
