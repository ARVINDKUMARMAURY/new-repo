import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Credentials
    API_ID = int(os.getenv("API_ID", "39917988"))
    API_HASH = os.getenv("API_HASH", "bd827dbeac6a55896ff11539bc80365b")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8522799922:AAF3-8heGrCM7UZuSTm1ttmfLVDLAAlrDo8")
    
    # Admin Credentials
    OWNER_ID = int(os.getenv("OWNER_ID", "7875184322"))
    LOGGER_ID = int(os.getenv("LOGGER_ID", "-1003781924669"))
    
    # Storage
    STORAGE_CHAT_ID = int(os.getenv("STORAGE_CHAT_ID", "-1003577577725"))
    STRING_SESSION = os.getenv("STRING_SESSION", "")
    
    # API Configuration
    API_KEY = os.getenv("API_KEY", "ADMINBABYX_63C6BB96432E3D6B2E217D29F695EBD6D93D4CFA")
    BASE_URL = os.getenv("BASE_URL", "https://api.babiesiq.tech")
    
    # Bot Configuration
    BOT_NAME = os.getenv("BOT_NAME", "MyBot")
    DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "500"))
    QUEUE_LIMIT = int(os.getenv("QUEUE_LIMIT", "100"))
    
    # Database
    MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "bot_db")