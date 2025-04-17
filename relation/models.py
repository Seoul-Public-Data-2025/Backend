from django.db import models
from user.models import CustomUser

class Relation(models.Model):
    '''
    1. 자녀(requester)가 부모를 등록 후 요청 -> 부모(target)가 수락
    2. 부모(requester)가 자녀를 등록 후 요청 -> 자녀(target)가 수락
    '''
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requester') # 등록을 요청한 사람
    is_approved = models.BooleanField(default=False) # 수락 여부
    created_at = models.DateTimeField(auto_now_add=True)

    # 부모-자녀 등록 시에만 사용할 이름, 연락처... ?
    # 등록을 수락할 사람의 이름, 연락처
    target_name = models.CharField(max_length=20, null=False, blank=False)
    target_phone = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        unique_together = ('requester', 'target_name', 'target_phone') # 동일 관계 중복 방지


