from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from .serializers import VendorSerializer





class VendorAPIView(APIView):
    def post(self,request):
        data = request.data
        user_id = request.user.id
        data['user'] = user_id
        serializer = VendorSerializer (data=data)
        if serializer.is_valid():
            vendor_data = serializer.save()
            return Response({
                "status" : status.HTTP_201_CREATED,
                "vendor_data": vendor_data.data
            },status.HTTP_201_CREATED)
            
        return Response({
                "status" : status.HTTP_403_FORBIDDEN,
                "vendor_data": serializer.errors
            },status.HTTP_403_FORBIDDEN)
