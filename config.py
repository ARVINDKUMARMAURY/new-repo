import os

# ===================== Telegram =====================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ===================== Database =====================
MONGO_URL = os.getenv("MONGO_URL", "")

# ===================== Log Group =====================
# Bot start + song play + error alerts sab yahan jaayenge
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))

# ===================== BabyAPI (song/video fetch source) =====================
BASE_URL = os.getenv("BASE_URL", "https://api.babiesiq.tech")
API_KEY = os.getenv("API_KEY", "")

# ===================== Permanent NVMe Storage =====================
STORAGE_DIR = os.getenv("STORAGE_DIR", "/root/vps_songs")

# ===================== Limits =====================
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "18000"))   # seconds, 5 hours
QUEUE_LIMIT = int(os.getenv("QUEUE_LIMIT", "30"))             # max songs per chat queue
