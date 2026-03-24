import os

# X (Twitter) API Keys
X_API_KEY = os.getenv("X_API_KEY", "")
X_API_KEY_SECRET = os.getenv("X_API_KEY_SECRET", "")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN", "")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET", "")

# Anthropic API Key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Threads API (Meta Graph API)
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "")
THREADS_USER_ID = os.getenv("THREADS_USER_ID", "")

# System Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POST_INTERVAL_HOURS = 8  # 1日3回 (24/3)
POST_QUEUE_FILE = os.path.join(BASE_DIR, "post_queue.json")
DRAFT_QUEUE_FILE = os.path.join(BASE_DIR, "draft_queue.json")
LOG_FILE = os.path.join(BASE_DIR, "x_auto.log")
