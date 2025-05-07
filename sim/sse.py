# sim/sse.py
import asyncio
from collections import defaultdict

# 채널별 메시지 큐 저장소
channel_queues = defaultdict(asyncio.Queue)

def get_channel_queue(channel_name):
    return channel_queues[channel_name]

def remove_channel_queue(channel_name):
    if channel_name in channel_queues:
        del channel_queues[channel_name]
