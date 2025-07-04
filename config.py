import os

class Config:
    # Require
    BOT_OWNER = int(os.environ.get("BOT_OWNER", ""))
    APP_ID = int(os.environ.get("APP_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    LOGS_CHANNEL = int(os.environ.get("LOGS_CHANNEL", ""))
    MONGODB_URL = os.environ.get("MONGODB_URL", "")
    MONGODB_DBNAME = os.environ.get("MONGODB_DBNAME", "")
