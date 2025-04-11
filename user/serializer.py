from rest_framework import serializers
from .models import CustomUser
class KakaoCodeSerializer(serializers.ModelSerializerSerializer):
    code = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ["email"]