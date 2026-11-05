import redis
import os

redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)

def get_cached_summary(video_id: str):
    return redis_client.get(f"summary:{video_id}")


def cache_summary(video_id: str, summary: str):
    redis_client.setex(
        f"summary:{video_id}",
        86400,  # 24 hours
        summary
    )