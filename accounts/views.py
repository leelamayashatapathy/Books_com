from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from rest_framework.permissions import AllowAny


from .serializers import UserSerializer

from .utils import get_token_for_user,send_otp_sms





class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save(is_active=False, is_registration_pending=True)
            user.generate_otp()
            # send_otp_email(user)
            if user.phone:
                print(user.phone)
                send_otp_sms(user)

            return Response({
                "status": True,
                "message": "OTP sent to your email/phone. Please verify to complete registration."
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status.HTTP_400_BAD_REQUEST)
        
        
        
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email, is_registration_pending=True)
        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "No pending registration found."
            }, status.HTTP_404_NOT_FOUND)

        if user.otp != str(otp):
            return Response({
                "status": False,
                "message": "Invalid OTP."
            }, status=400)

        if user.otp_expired():
            return Response({
                "status": False,
                "message": "OTP expired."
            }, status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.is_registration_pending = False
        user.otp = None
        user.otp_created_at = None
        user.save()

        token = get_token_for_user(user)

        return Response({
            "status": True,
            "message": "Registration verified successfully.",
            "token": token
        }, status.HTTP_200_OK)


            
            
            


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user:
            tokens = get_token_for_user(user)
            return Response({
                "status": True,
                "message": "Login successful",
                "user": UserSerializer(user).data,
                "token": tokens
            })
        return Response({
            "status": False,
            "message": "Invalid credentials"
        }, status.HTTP_400_BAD_REQUEST)
            