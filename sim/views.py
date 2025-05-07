# sim/views.py
from django.http import StreamingHttpResponse
from sim.sse import get_channel_queue
import json
import asyncio

async def sse_stream(request, uid):
    channel_name = f"child-{uid}"
    queue = get_channel_queue(channel_name)

    async def event_stream():
        while True:
            data = await queue.get()
            yield f"data: {json.dumps(data)}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

# sim/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.hash import hash_uid
from utils.fcm import send_fcm_notification
from relation.models import Channel, Relation
from django.db.models import F
from sim.sse import get_channel_queue

class ChildLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        child_email = request.user.email
        time = request.data.get("time")
        lat = request.data.get("lat")
        lot = request.data.get("lot")

        if not child_email or not time or not lat or not lot:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        uid = hash_uid(str(request.user.id))
        channel_name = f"child-{uid}"

        rel_list = Relation.objects.filter(
            child=request.user,
            is_approved=True,
            parent_user__fcmToken__isnull=False
        ).annotate(
            fcm=F('parent_user__fcmToken'),
            child_name=F('childName')
        ).values('fcm', 'child_name')

        if not self.is_channel_open(channel_name):
            for rel in rel_list:
                send_fcm_notification(
                    token=rel['fcm'],
                    title="긴급상황",
                    body=f"{rel['child_name']}님이 긴급 버튼을 눌렀습니다.",
                    data={
                        "type": "child-location",
                        "url": f"/events/child/{uid}/"
                    }
                )

        queue = get_channel_queue(channel_name)
        queue.put_nowait({
            "type": "location",
            "childEmail": child_email,
            "time": time,
            "lat": lat,
            "lot": lot
        })

        return Response({
            'success': True,
            'result': {
                'message': '위치를 전송했습니다.',
                'url': f"/events/child/{uid}/"
            }
        }, status=status.HTTP_200_OK)

    def is_channel_open(self, channel_name):
        from relation.models import Channel
        try:
            channel_status = Channel.objects.get(channel_name=channel_name)
            if not channel_status.is_open:
                channel_status.is_open = True
                channel_status.save()
                return False
            return True
        except Channel.DoesNotExist:
            Channel.objects.create(channel_name=channel_name, is_open=True)
            return False
        

class ChildDisconnectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        uid = hash_uid(str(request.user.id))
        channel_name = f"child-{uid}"

        queue = get_channel_queue(channel_name)
        queue.put_nowait({
            "type": "done",
            "message": "자녀가 연결을 종료했습니다."
        })

        Channel.objects.filter(channel_name=channel_name).update(is_open=False)

        return Response({
            'success': True,
            'result': {
                'message': '연결 종료 메시지를 전송했습니다.'
            }
        }, status=status.HTTP_200_OK)