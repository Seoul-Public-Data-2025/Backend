from rest_framework import serializers
from .models import CustomUser

class KakaoTokenSerializer(serializers.ModelSerializer):
    accessToken=serializers.CharField()
    class Meta:
        model = CustomUser
        fields=["email","accessToken","hashedPhoneNumber","image","profileName","fcmToken"]
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['notification']


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fcm_token']