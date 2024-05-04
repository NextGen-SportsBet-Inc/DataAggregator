import os
import redis
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Initialize Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD, decode_responses=True)


def ensure_connections():
    """
    Ensure connections to Redis.

    :return: None
    """
    if redis_client.ping():
        print("Connected to Redis")
    else:
        print("Could not connect to Redis")