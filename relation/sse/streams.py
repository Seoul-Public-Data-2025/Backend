from .manager import sse_manager
import json
def event_stream(child_id):
    queue = sse_manager.register(child_id)
    try:
        while True:
            data = queue.get()
            yield f"data: {json.dumps(data)}\n\n" #json.dumps로 직렬화, yiled로 코루틴
    except GeneratorExit:#코루틴 종료 시
        sse_manager.unregister(child_id, queue)
