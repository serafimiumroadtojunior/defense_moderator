import os
from typing import Optional

from dotenv import load_dotenv
from redis.asyncio import Redis

from app.bot.config import ENV_FILE

load_dotenv(dotenv_path=ENV_FILE)

password: Optional[str] = os.getenv('REDIS_PASSWORD')
if password is None:
    raise ValueError("Redis password is not set in environment variables")

async_redis: Redis = Redis(
    host='localhost', 
    port=6379,
    password=password,
    decode_responses=True
)