from collections import defaultdict
from queue import Queue
class SSEManager:
    def __init__(self):
        self.connections = defaultdict(list)  # child_id → [queue1, queue2, ...]

    def register(self, child_email):
        q = Queue()
        self.connections[child_email].append(q)
        return q

    def unregister(self, child_email, q):
        self.connections[child_email].remove(q)

    def send(self, child_email, data):
        for q in self.connections[child_email]:
            q.put(data)

sse_manager=SSEManager()