from src.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from src.logger import get_logger


log = get_logger()

class Database :
    def __init__(self):
        
        # connect
        self.client = AsyncIOMotorClient(settings.MONGO_DB_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        
        # collections
        self.users = self.db["users"]
        self.admins = self.db["admins"]
        self.channels = self.db["channels"]
        
        
    async def connect(self):
        try:
            await self.client.admin.command("ping")
            log.info("Connected to MongoDB")
        except Exception as e:
            log.error(f"Error connecting to MongoDB: {e}")
            
db = Database()