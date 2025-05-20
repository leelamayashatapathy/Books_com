from django.urls import path
from .views import RegistrationView,VerifyOTPView

urlpatterns = [
    path('user/registration/',RegistrationView.as_view(), name='registration'),
    path('user/verify-otp/',VerifyOTPView.as_view(), name='verify-otp'),
    
]