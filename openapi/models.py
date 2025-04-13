from django.db import models
from utils.constants import DISTRICT_CODE
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