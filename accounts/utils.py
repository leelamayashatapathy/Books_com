from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.conf import settings
from twilio.rest import Client


def get_token_for_user(user):
    refresh_ = RefreshToken.for_user(user)
    return({
        "refresh":str(refresh_),
        "access":str(refresh_.access_token)
    })
    
    
class CustomTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            # Optional: rotate refresh token (issue a new refresh token)
            # Uncomment the following lines if you want to blacklist old refresh tokens
            # refresh.blacklist()
            # new_refresh_token = str(refresh)

            return Response({
                'access': new_access_token,
                # 'refresh': new_refresh_token,  # If refresh rotation enabled
            }, status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    




def send_otp_sms(user):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Your OTP is {user.otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=user.phone
    )
