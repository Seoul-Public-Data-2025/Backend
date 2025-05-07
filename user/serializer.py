from rest_framework import serializers
from .models import CustomUser

class KakaoTokenSerializer(serializers.ModelSerializer):
    kakaoAccessToken=serializers.CharField()
    class Meta:
        model = CustomUser
        fields=["email","kakaoAccessToken","hashedPhoneNumber","fcmToken", "nickname", "profile"]
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['notification','hashedPhoneNumber']


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fcm_token']