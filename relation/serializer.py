from rest_framework import serializers
from relation.models import Relation
from django.core.exceptions import ObjectDoesNotExist
from user.models import CustomUser

class RelationRequestSerializer(serializers.Serializer):
    parentPhoneNumber = serializers.CharField(required=True, allow_blank=False)
    parentName = serializers.CharField(required=True, allow_blank=False)
    class Meta:
        model = Relation
        fields = ['parentPhoneNumber', 'parentName']

    def create(self, validated_data):
        child = self.context['request'].user
        parent_phone_number = validated_data.get('parentPhoneNumber')
        try:
            parent_user = CustomUser.objects.filter(hashedPhoneNumber=parent_phone_number).first()
        except ObjectDoesNotExist:
            raise serializers.ValidationError("해당 전화번호를 가진 보호자 유저가 존재하지 않습니다.")
        
        # 자녀가 이미 부모를 등록한 경우, 새로운 관계를 추가하지 않음
        if Relation.objects.filter(child=child, parent_user=parent_user).exists():
            raise serializers.ValidationError("이 사용자는 이미 해당 보호자와 관계가 등록되어 있습니다.")
        
        # Relation 객체 생성
        relation = Relation.objects.create(
            childName=child.nickname,
            parent_user=parent_user,  # 찾은 부모 유저를 설정
            parentName=validated_data['parentName'],
            child=child,  # 현재 로그인된 유저를 자녀로 설정
        )
        return relation

class RelationApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ['id', 'is_approved']