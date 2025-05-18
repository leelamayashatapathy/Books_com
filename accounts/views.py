from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

from .utils import get_token_for_user



class RegistrationView(APIView):
    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            token = get_token_for_user(instance)
            user_data = serializer.data
            
            return Response({
                "status" : status.HTTP_200_OK,
                "message" : "User Registred successfully",
                "user" :user_data,
                "token" : token
            })
        else:
            return Response({
                "status" : status.HTTP_400_BAD_REQUEST,
                "message" : "User Registration failed",
                "user" :serializer.errors,
            })
            