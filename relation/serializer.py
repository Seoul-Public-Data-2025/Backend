from rest_framework import serializers
from relation.models import Relation

class RelationRequestSerializer(serializers.ModelSerializer):
    target_name = serializers.CharField(write_only=True)
    target_phone = serializers.CharField(write_only=True)

    class Meta:
        model = Relation
        fields = ['target_name', 'target_phone']

    def create(self, validated_data):
        requester = self.context['request'].user

        return Relation.objects.create(
            requester=requester,
            target_name=validated_data['target_name'],
            target_phone=validated_data['target_phone']
        )

class RelationApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ['id', 'is_approved']