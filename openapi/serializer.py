from rest_framework import serializers
from .models import CCTV, SafetyFacility, SafetyService
from utils.constants import DISTRICT_CODE

class CCTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ['id', 'district', 'lat', 'lot', 'addr']

class SafetyFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyFacility
        fields = '__all__'

class SafetyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyService
        fields = '__all__'