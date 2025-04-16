from django.db import models
from utils.constants import DISTRICT_CODE, FACILITY_TYPE, SERVICE_TYPE, DISPLAY_FACILITY_TYPE


class CCTV(models.Model):
    district=models.CharField('District',max_length=10,choices=DISTRICT_CODE)
    lat=models.DecimalField(max_digits=11,decimal_places=8)
    lot=models.DecimalField(max_digits=11,decimal_places=8)
    addr=models.CharField(max_length=255)
    class Meta:
        unique_together = (('lat', 'lot'),('district','lat','lot','addr'))
    
class PoliceOffice(models.Model):
    officeName=models.CharField('OfficeName',max_length=255)
    lat=models.DecimalField(max_digits=11,decimal_places=8)
    lot=models.DecimalField(max_digits=11,decimal_places=8)
    addr=models.CharField(max_length=255)
    class Meta:
        unique_together = (('lat', 'lot'),('officeName','lat','lot','addr'))

class SafetyFacility(models.Model):
    facility_id = models.CharField(max_length=50, unique=True) # 시설물코드 (같은 위치 CCTV의 경우 덮어쓰기가 됨, 그래서 시설물코드로 구분)
    facility_type = models.CharField(max_length=10, choices=FACILITY_TYPE, default="301") # 301 : 안심벨
    facility_latitude = models.DecimalField(max_digits=11,decimal_places=8)
    facility_longitude = models.DecimalField(max_digits=11,decimal_places=8)
    facility_location = models.TextField(null=False)
    sigungu_code = models.CharField(max_length=20, null=False)
    sigungu_name = models.CharField(max_length=20, null=False)
    eupmyeondong_code = models.CharField(max_length=20, null=False)
    eupmyeondong_name = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.facility_type} - {self.sigungu_name} {self.eupmyeondong_name}'

class SafetyService(models.Model):
    service_id = models.CharField(max_length=50, unique=True) # 시설물코드 (같은 위치 CCTV의 경우 덮어쓰기가 됨, 그래서 시설코드로 구분)
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE, default="401") # 401 : 안심택배함
    service_latitude = models.DecimalField(max_digits=11,decimal_places=8)
    service_longitude = models.DecimalField(max_digits=11,decimal_places=8)
    service_location = models.TextField(null=False)
    sigungu_code = models.CharField(max_length=20, null=False)
    sigungu_name = models.CharField(max_length=20, null=False)
    eupmyeondong_code = models.CharField(max_length=20, null=False)
    eupmyeondong_name = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.service_type} - {self.sigungu_name} {self.eupmyeondong_name}'

class DisplayIcon(models.Model):
    facility_type= models.CharField(max_length=10,choices=DISPLAY_FACILITY_TYPE),
    lat=models.DecimalField(max_digits=11,decimal_places=8)
    lot=models.DecimalField(max_digits=11,decimal_places=8)
    addr=models.CharField(max_length=255, null=True, blank=True)