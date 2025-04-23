from django.shortcuts import render
from utils.permission import HasHashedPhoneNumber
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from relation.models import Relation
from relation.serializer import RelationRequestSerializer, RelationApproveSerializer
from firebase_admin import messaging
from utils.fcm import send_fcm_notification

class RelationRequestView(APIView): # 부모-자녀 등록 요청
    permission_classes = [HasHashedPhoneNumber,IsAuthenticated]
    def post(self, request):
        serializer = RelationRequestSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            relation=serializer.save()
            parent_user = relation.parent_user
            if parent_user.fcmToken:
                send_fcm_notification(token=parent_user.fcmToken,
                                      title="관계요청",
                                      body=f"{relation.child.profileName}님이 보호자 등록을 요청했습니다.",
                                      data={
                                          "type":"regist",
                                          "id":relation.id
                                      })
            return Response({
                'success': True,
                'result': {
                    'id':relation.id,
                    'message': '알림을 전송했습니다.'
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class ResendNotificationView(APIView):
    def post(self, request):
        relation_id = request.data.get("id")

        if not relation_id:
            return Response({
                "success": False,
                "message": "관계 id가 요청에 포함되어야 합니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            relation = Relation.objects.get(id=relation_id)
        except Relation.DoesNotExist:
            return Response({
                "success": False,
                "message": "해당 관계 요청이 존재하지 않습니다."
            }, status=status.HTTP_404_NOT_FOUND)
            
        parent_user = relation.parent_user
        
        if not parent_user.fcmToken:
            return Response({
                "success": False,
                "message": "보호자의 FCM 토큰이 존재하지 않습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        send_fcm_notification(
            token=parent_user.fcmToken,
            title="관계요청",
            body=f"{relation.child.profileName}님이 보호자 등록을 요청했습니다.",
            data={
                "type": "parent",
                "id": relation.id
            }
        )
        
        return Response({
            "success": True,
            "message": "알림을 재전송했습니다."
        }, status=status.HTTP_200_OK)

class RelationApproveView(APIView): # 부모-자녀 등록 수락
    permission_classes=[IsAuthenticated]
    def post(self, request): # fcm 연동
        relation_id = request.data.get("id")

        if not relation_id:
            return Response({
                "success": False,
                "message": "관계 id가 요청에 포함되어야 합니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            relation = Relation.objects.get(id=relation_id)
        except Relation.DoesNotExist:
            return Response({
                'success': False,
                'message': '해당 관계를 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)
            
        # 본인이 수락 대상인지 검증
        if request.user != relation.parent_user:
            return Response({
                'success': False,
                'message': '요청을 수락할 권한이 없습니다.'
            }, status=status.HTTP_403_FORBIDDEN)

        # 이미 수락된 요청인지 확인
        if relation.is_approved:
            return Response({
                'success': False,
                'message': '이미 수락된 요청입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 수락 처리
        relation.is_approved = True
        relation.save()

        return Response({
            'success': True,
            'result': {
                'message': '요청을 성공적으로 수락했습니다.',
                'id':relation.id
            }
        }, status=status.HTTP_200_OK)
        

class RelationRoleListView(APIView):
    def get(self, request):
        user = request.user

        # 보호자인 관계들
        as_parent = Relation.objects.filter(parent_user=user, is_approved=True)
        parent_relations = [{
            "id": rel.id,
            "name": rel.child.profileName,
            "phone": rel.child.hashedPhoneNumber,
            "role": "parent",
            "isApproved": rel.is_approved
        } for rel in as_parent]

        # 피보호자인 관계들
        as_child = Relation.objects.filter(child=user, is_approved=True)
        child_relations = [{
            "id": rel.id,
            "name": rel.parent_user.profileName,
            "phone": rel.parent_user.hashedPhoneNumber,
            "role": "child",
            "isApproved": rel.is_approved
        } for rel in as_child]

        return Response({
            "success": True,
            "result": {
                "relations": parent_relations + child_relations
            }
        }, status=status.HTTP_200_OK)

class RelationUpdateNameView(APIView):
    def patch(self,request):
        user=request.user
        
        new_name=request.data.get("name")
        
        if not new_name:
            return Response({
                'success':False,
                'message':"이름을 입력하세요"
            },status=status.HTTP_400_BAD_REQUEST)
            
        relation_id = request.data.get("id")

        if not relation_id:
            return Response({
                "success": False,
                "message": "관계 id가 요청에 포함되어야 합니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            relation = Relation.objects.get(id=relation_id, is_approved=True)
        except Relation.DoesNotExist:
            return Response({
                "success": False,
                "message": "해당 관계를 찾을 수 없습니다."
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 사용자 입장 따라 어떤 이름을 바꿀지 결정
        if relation.child == user:
            relation.parentName = new_name
        elif relation.parent_user == user:
            relation.childName = new_name
        else:
            return Response({
                "success": False,
                "message": "이 관계에 대한 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)

        relation.save()
        
        return Response({
            "success": True,
            "result": {
                "message": "이름이 성공적으로 변경되었습니다.",
                "relation_id": relation.id
            }
        }, status=status.HTTP_200_OK)
        
class RelationDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self,request):
        relation_id = request.data.get("id")
        if not relation_id:
            return Response({
                "success": False,
                "message": "관계 id가 요청에 포함되어야 합니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            relation = Relation.objects.get(id=relation_id)
        except Relation.DoesNotExist:
            return Response({
                "success": False,
                "message": "해당 관계가 존재하지 않습니다."
            }, status=status.HTTP_404_NOT_FOUND)
            
        if request.user != relation.child:
            return Response({
                "success": False,
                "message": "삭제 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)
        parent_user = relation.parent_user
        relation.delete()
        send_fcm_notification(
            token=parent_user.fcmToken,
            title="관계삭제",
            body=f"{relation.child.profileName}님이 보호자 등록을 취소했습니다.",
            data={
                "type": "delete",
                "id": relation.id
            }
        )
        return Response({
            "success": True,
            "message": "관계가 성공적으로 삭제되었습니다."
        }, status=status.HTTP_204_NO_CONTENT)