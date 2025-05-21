from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from.models import VendorAddress


from .serializers import VendorSerializer,VendorAddressSerializer





class VendorAPIView(APIView):
    def post(self,request):
        data = request.data
        user_id = request.user.id
        data['user'] = user_id
        serializer = VendorSerializer (data=data)
        if serializer.is_valid():
            vendor_data = serializer.save()
            v_data = VendorSerializer(vendor_data)
            return Response({
                "status" : status.HTTP_201_CREATED,
                "vendor_data": v_data.data
            },status.HTTP_201_CREATED)
            
        return Response({
                "status" : status.HTTP_403_FORBIDDEN,
                "vendor_data": serializer.errors
            },status.HTTP_403_FORBIDDEN)
        
        
class VendorAddressApiView(APIView):
    
    def post(self, request):
        data = request.data
        user = request.user
        vendor = user.vendor_profile.id
        data['vendor'] = vendor
        serializer = VendorAddressSerializer(data=data)
        if serializer.is_valid():
            insatnce = serializer.save()
            vendor_address = VendorAddressSerializer(insatnce).data
            return Response({
                "status": True,
                "message": "vendor Address Added successfully",
                "user": vendor_address
            })
        return Response({
            "status": False,
            "message": "Bad request",
            "error": serializer.errors
        }, status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        user = request.user
        data = request.data
        add_id = data.get('id')
        vendor = user.vendor_profile.id
        data['vendor'] = vendor 
        query = VendorAddress.objects.get(id=add_id, user=user)
        serializer =VendorAddressSerializer(query,data,partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            add_data = VendorAddressSerializer(instance).data
            return Response({
                "status": True,
                "message": "User Address updated successfully",
                "user": add_data
            })
        return Response({
            "status": False,
            "message": "Bad request",
            "error": serializer.errors
        }, status.HTTP_400_BAD_REQUEST)
