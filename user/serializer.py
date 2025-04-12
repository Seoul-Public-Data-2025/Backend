from rest_framework import serializers
from .models import CustomUser
class KakaoTokenSerializer(serializers.ModelSerializer):
    accessToken=serializers.CharField()
    class Meta:
        model = CustomUser
        fields=["email","accessToken"]