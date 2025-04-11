from rest_framework import serializers
class KakaoCodeSerializer(serializers.Serializer):
    code = serializers.CharField()