from django.urls import path,include
from .views import VendorAPIView

urlpatterns = [
    path('vendor/details/',VendorAPIView.as_view(), name='vendor-details'),
]