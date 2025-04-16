from rest_framework import serializers
from .models import CCTV, SafetyFacility, SafetyService, PoliceOffice, DisplayIcon
from utils.constants import DISTRICT_CODE

class CCTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ['id', 'district', 'lat', 'lot', 'addr']

class PoliceOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceOffice
        fields = ['id','officeName','lat','lot','addr']
class SafetyFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyFacility
        fields = '__all__'

class SafetyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyService
        fields = '__all__'
        
class DisplayIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayIcon
        fields = '__all__'