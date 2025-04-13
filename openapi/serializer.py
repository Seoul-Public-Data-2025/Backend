from rest_framework import serializers
from .models import CCTV,PoliceOffice
from utils.constants import DISTRICT_CODE

class CCTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ['id', 'district', 'lat', 'lot', 'addr']

class PoliceOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PoliceOffice
        fields=['id','officeName','lat','lot','addr']