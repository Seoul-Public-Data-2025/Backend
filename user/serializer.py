from rest_framework import serializers
from .models import CustomUser
class KakaoCodeSerializer(serializers.ModelSerializer):
    #code = serializers.CharField()
    accessToken=serializers.CharField()
    refreshToken=serializers.CharField()
    class Meta:
        model = CustomUser
        #fields = ["code","email"]
        fields=["email","accessToken","refreshToken"]