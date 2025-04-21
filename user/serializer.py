from rest_framework import serializers
from .models import CustomUser

class KakaoTokenSerializer(serializers.ModelSerializer):
    accessToken=serializers.CharField()
    class Meta:
        model = CustomUser
        fields=["email","accessToken"]
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['notification']

# TODO: FCM 완료 후 주석 해제
# class FCMTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['fcm_token']