from rest_framework import serializers
from . models import User,UserAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'is_vendor']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            phone=validated_data.get('phone'),
            password=validated_data.get('password'),
            is_vendor=validated_data.get('is_vendor', False)
        )
        return user
    
    
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"