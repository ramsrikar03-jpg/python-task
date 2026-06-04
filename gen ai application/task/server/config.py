import os
from pathlib import Path

from dotenv import load_dotenv

# Always load .env from project root (task/), not from the shell cwd
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "movie_ticket_booking")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
