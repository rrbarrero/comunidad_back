import json
import redis
from django.conf import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=1)

def publish_event(channel_name, data_msg):
    redis_client.publish(channel_name, json.dumps(data_msg))