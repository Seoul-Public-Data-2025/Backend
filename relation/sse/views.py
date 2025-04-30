from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from .streams import event_stream

class GuardianSSEView(APIView):
    def get(self, request, child_id):
        response = StreamingHttpResponse(event_stream(child_id), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response