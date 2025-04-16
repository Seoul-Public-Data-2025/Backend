from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from relation.models import Relation
from relation.serializer import RelationRequestSerializer, RelationApproveSerializer

class RelationRequestView(APIView): # 부모-자녀 등록 요청
    def post(self, request):
        serializer = RelationRequestSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'result': {
                    'message': 'The request has been sent successfully.'
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'The request failed.'
        }, status=status.HTTP_400_BAD_REQUEST)


class RelationApproveView(APIView): # 부모-자녀 등록 수락
     def post(self, request, relation_id): # fcm 연동
        try:
            relation = Relation.objects.get(id=relation_id)
        except Relation.DoesNotExist:
            return Response({
                'success': False,
                'message': 'The request does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

        relation.is_approved = True
        relation.save()
        return Response({
            'success': True,
            'result' : {
                'message': 'The request has been approved.'
            }
        }, status=status.HTTP_200_OK)


class RelationListView(APIView): # 부모-자녀 등록 목록 조회
    def get(self, request):
        user = request.user

        # 수락된 관계만 필터링
        relations = Relation.objects.filter(
            is_approved=True
        ).filter(
            Q(requester=user) | Q(target=user)
        )

        result = []
        for rel in relations:
            result.append({
                "name": rel.target_name,
                "phone": rel.target_phone,
            })

        return Response({
            'success': True,
            'result': {
                'relation' : result
            }
        }, status=status.HTTP_200_OK)
