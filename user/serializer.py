from rest_framework import serializers
from .models import CustomUser
class KakaoCodeSerializer(serializers.ModelSerializer):
    #code = serializers.CharField()
    access_token=serializers.CharField()
    refresh_token=serializers.CharField()
    class Meta:
        model = CustomUser
        #fields = ["code","email"]
        fields=["email","access_token","refresh_token"]