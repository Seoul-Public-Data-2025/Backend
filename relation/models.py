from django.db import models
from user.models import CustomUser

class Relation(models.Model):
    
    child = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requester') # 피보호자
    childName = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=False) # 수락 여부
    created_at = models.DateTimeField(auto_now_add=True)
    parent_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='target') # 보호자
    parentName = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('child', 'parentName') # 동일 관계 중복 방지