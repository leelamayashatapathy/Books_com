from django.urls import path,include
from .views import VendorAPIView,VendorAddressApiView

urlpatterns = [
    path('vendor/details/',VendorAPIView.as_view(), name='vendor-details'),
    path('vendor/address/',VendorAddressApiView.as_view(), name='vendor-address'),
    
]