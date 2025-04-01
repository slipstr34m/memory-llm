import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PG_CONN_URL = os.getenv("PG_CONN_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASS = os.getenv("REDIS_PASS", None)
REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")