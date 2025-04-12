from rest_framework import serializers
from .models import CCTV
from utils.constants import DISTRICT_CODE

class CCTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ['id', 'district', 'lat', 'lot', 'addr']