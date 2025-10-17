from src.database.connection import db
from src.logger import get_logger
from datetime import datetime

log = get_logger()

class Channel:
    collection = db.channels
    
    @classmethod
    async def add_channel(cls , chat_id : int , title : str = None):
        try:
            await cls.collection.insert_one({"channel_id" : chat_id , "title" : title , "added_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        except Exception as e:
            log.error(f"Error adding channel: {e}")
            
    @classmethod
    async def remove_channel(cls , chat_id : int):
        try:
            await cls.collection.delete_one({"channel_id" : chat_id})
        except Exception as e:
            log.error(f"Error removing channel: {e}")
            
    @classmethod
    async def get_all(cls):
        try:
            cursor = cls.collection.find({})
            return [doc async for doc in cursor]
        except Exception as e:
            log.error(f"Error getting all channels: {e}")
            
    @classmethod   
    async def get_channel(cls, channel_id: int):
        try:
            return await cls.collection.find_one({"channel_id": channel_id})
        except Exception as e:
            log.error(f"Error getting channel: {e}")