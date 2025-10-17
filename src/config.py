from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    MONGO_DB_URI: str = os.getenv("MONGO_DB_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
settings = Settings()