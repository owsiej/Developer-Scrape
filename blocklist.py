import redis

BLOCKLIST = redis.Redis(host="redis", decode_responses=True, db=0)
