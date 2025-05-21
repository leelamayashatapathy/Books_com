from rest_framework import serializers
from .models import Vendor,VendorAddress



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
        
    def create(self, validated_data):
        vendor = Vendor.objects.create(**validated_data)
        return vendor
    
    
class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = "__all__"