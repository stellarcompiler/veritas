import redis

r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True
)

try:
    print("PING:", r.ping())
except redis.ConnectionError as e:
    print("Redis connection failed:", e)
