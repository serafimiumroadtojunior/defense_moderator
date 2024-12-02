import os
from typing import Optional

from dotenv import load_dotenv
from aioredis import Redis

load_dotenv(dotenv_path=os.path.join("defense_moderator", ".env"))

password: Optional[str] = os.getenv('REDIS_PASSWORD')
if password is None:
    raise ValueError("Redis password is not set in environment variables")

async_redis: Redis = Redis(
    host='localhost', 
    port=6379,
    password=password
)