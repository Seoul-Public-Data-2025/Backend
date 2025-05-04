from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_eventstream import send_event
from utils.hash import hash_uid
from utils.fcm import send_fcm_notification
from relation.models import Channel,Relation

class ChildLocationView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        child_email = request.user.email
        time = request.data.get("time")
        lat = request.data.get("lat")
        lot = request.data.get("lot")

        if not child_email or not time or not lat or not lot:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
        channel_name=f"child-{hash_uid(str(request.user.id))}"
        
        rel_list=Relation.objects.filter(child=request.user,is_approved=True,parent_user__fcmToken__isnull=False).values(fcm='parent_user__fcmToken',child_name='childName')
        
        if not self.is_channel_open(channel_name):
            # 채널이 처음 열리면 FCM 보내기
            for rel in rel_list:
                send_fcm_notification(
                    token=rel['fcm'],
                    title="긴급상황",
                    body=f"{rel['child_name']}님이 긴급 버튼을 눌렀습니다.",
                    data={
                        "url":f"events/child/{channel_name}/",
                    }
                )
        
        # send_event(<channel>, <event_type>, <event_data>) 채널큐에 메시지 저장
        send_event(channel_name, "location", {
            "childEmail":child_email,
            "time": time,
            "lat": lat,
            "lot": lot
        })

        return Response({
                'success': True,
                'result': {
                    'message': '위치를 전송했습니다.'
                }
            }, status=status.HTTP_200_OK)
        
    def is_channel_open(self, channel_name):
        try:
            channel_status = Channel.objects.get(channel_name=channel_name)
            return channel_status.is_open
        except Channel.DoesNotExist:
            Channel.objects.create(channel_name=channel_name, is_open=True)
            return False

class ChildDisconnectView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        channel_name=f"child-{hash_uid(str(request.user.id))}"
        # send_event(<channel>, <event_type>, <event_data>) 채널큐에 메시지 저장
        send_event(channel_name, "done", {
            "message": "자녀가 연결을 종료했습니다."
        })
        
        Channel.objects.filter(channel_name=channel_name).update(is_open=False)

        return Response({
                'success': True,
                'result': {
                    'message': '연결 종료 메시지를 전송했습니다.'
                }
            }, status=status.HTTP_200_OK)
        