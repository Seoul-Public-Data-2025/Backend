from django.shortcuts import render
from utils.permission import HasHashedPhoneNumber
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from relation.models import Relation
from relation.serializer import RelationRequestSerializer, RelationApproveSerializer
from firebase_admin import messaging

class RelationRequestView(APIView): # 부모-자녀 등록 요청
    permission_classes = [HasHashedPhoneNumber]
    def post(self, request):
        serializer = RelationRequestSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            relation=serializer.save()
            parent_user = relation.parent_user
            if parent_user.fcmToken:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="관계 요청",
                        body=f"{relation.child.profileName}님이 보호자 등록을 요청했습니다.",
                    ),
                    token=parent_user.fcmToken,
                )
                try:
                    messaging.send(message)
                except Exception as e:
                    # 로그만 찍고 실패해도 관계는 저장
                    print("FCM 전송 실패:", e)
            return Response({
                'success': True,
                'result': {
                    'message': 'The request has been sent successfully.'
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
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