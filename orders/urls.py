from django.urls import path
from .views import CartApiView,OrderApiView

urlpatterns = [
    path('user/add-to-cart/',CartApiView.as_view(), name='add-to-cart'),
    path('user/order/',OrderApiView.as_view(), name='order'),
    
]