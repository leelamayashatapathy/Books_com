from django.urls import path
from .views import CartApiView

urlpatterns = [
    path('user/add-to-cart/',CartApiView.as_view(), name='add-to-cart'),
    
]