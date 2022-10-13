import base64
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .serializers import UsersSerializer
from .models import User
from customScript.customResponse import ResponseInfo
from customScript.customPagination import CustomZeroPagination
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenObtainPairSerializer,
)
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
import pyotp
from django.core.mail import send_mail
from dating.settings import EMAIL_HOST_USER
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "S3CR3T_P@55W0RD"


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, email=None, **kwargs):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class LoginIndex(APIView):
    permission_classes = []

    @staticmethod
    def get(request, emailID):
        try:
            Email = User.objects.get(email=emailID)
        except User.DoesNotExist:
            Email = User.objects.create_user(email=emailID)
        except ObjectDoesNotExist:
            raise ValidationError(
                {
                    "responseCode": "404",
                    "responseText": "failed",
                    "responseData": "No Email Found.",
                    "redirect": False,
                }
            )
        Email.counter += 1
        Email.save()
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(emailID).encode())
        OTP = pyotp.HOTP(key)
        subject = "OTP SEND"
        msg = f"You're OTP is {OTP.at(Email.counter)}"
        send_to = emailID
        send_mail(subject, msg, EMAIL_HOST_USER, [send_to], fail_silently=False)
        data = {
            "responseCode": "200",
            "responseText": "success",
            "error": {},
            "responseData": "OTP SEND SUCCESSFULLY.",
            "redirect": True,
        }
        return Response(data=data, status=200)

    def post(self, request, emailID):
        try:
            Email = User.objects.get(email=emailID)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(emailID).encode())
        OTP = pyotp.HOTP(key)
        if OTP.verify(request.data["otp"], Email.counter):
            if not Email.is_verified:
                print("-=-" * 30)
                Email.counter += 1
                Email.save()
                pyotp.HOTP(key)
                user = PasswordlessAuthBackend.authenticate(self, email=emailID)
                is_Login = RefreshToken.for_user(user)
                data = {
                    "responseCode": "200",
                    "responseText": "success",
                    "responseData": "Welcome to Dating App.",
                    "goingToDashBoard": False,
                    "token": {
                        "refresh_token": str(is_Login),
                        "access_token": str(is_Login.access_token),
                    },
                    "redirect": True,
                }
                return Response(data=data, status=200)
            if Email:
                print("-" * 30)
                print(Email.is_verified)
                Email.is_verified = True
                print("-" * 30)
                Email.counter += 1
                Email.save()
                pyotp.HOTP(key)
                user = PasswordlessAuthBackend.authenticate(self, email=emailID)
                is_Login = RefreshToken.for_user(user)
                data = {
                    "responseCode": "200",
                    "responseText": "success",
                    "responseData": "You are authorised.",
                    "goingToDashBoard": True,
                    "token": {
                        "refresh_token": str(is_Login),
                        "access_token": str(is_Login.access_token),
                    },
                    "redirect": True,
                }
                return Response(data=data, status=200)
        data = {
            "responseCode": "400",
            "responseText": "failed",
            "responseData": "OTP EXPIRED.",
            "token": {},
            "redirect": False,
        }
        return Response(data=data, status=400)


class UserCreateIndex(APIView):
    @staticmethod
    def post(request):
        try:
            email = request.data["email"]
            print(request.data['email'])
            user = User.objects.get(email=email)
            if not user.first_name:
                user.dob = request.data["dob"]
                user.first_name = request.data["first_name"]
                user.last_name = request.data["last_name"]
                user.save()
                context_data = {
                    "message": "success",
                    "error": None,
                    "data": "User Created.",
                }
                return Response(data=context_data, status=status.HTTP_200_OK)
            else:
                context_data = {
                    "message": "failed",
                    "error": status.HTTP_400_BAD_REQUEST,
                    "data": "You can't change user data now.",
                }
                return Response(data=context_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            context_data = {
                "message": "failed",
                "error": status.HTTP_400_BAD_REQUEST,
                "data": "User Not Found.",
            }
            return Response(data=context_data, status=status.HTTP_400_BAD_REQUEST)


class UserMeIndex(APIView):
    @staticmethod
    def get(request):
        query = User.objects.filter(id=request.user.id)
        serializer_class = UsersSerializer(query, many=True, context={"request": request})
        context_data = {
            "message": "success",
            "error": None,
            "data": serializer_class.data,
        }
        return Response(data=context_data, status=status.HTTP_200_OK)
