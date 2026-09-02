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

BOT_NAME = os.getenv("BOT_NAME", "Avisha")


class Config:
    """Same values as above, exposed as a class (some modules import it this way)."""
    API_ID = API_ID
    API_HASH = API_HASH
    BOT_TOKEN = BOT_TOKEN
    SESSION_STRING = SESSION_STRING
    OWNER_ID = OWNER_ID
    MONGO_URL = MONGO_URL
    LOG_GROUP_ID = LOG_GROUP_ID
    BASE_URL = BASE_URL
    API_KEY = API_KEY
    STORAGE_DIR = STORAGE_DIR
    DURATION_LIMIT = DURATION_LIMIT
    QUEUE_LIMIT = QUEUE_LIMIT
    BOT_NAME = BOT_NAME
