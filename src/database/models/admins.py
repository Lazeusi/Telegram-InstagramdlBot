from src.database.connection import db
from src.logger import get_logger
from datetime import datetime


log = get_logger()


class Admin:
    
    collection = db.admins
    
    @classmethod
    async def add_admin(cls, user_id: int, username: str = None, promoted_by = None):
        try:
            # Check if already admin
            existing = await cls.collection.find_one({"user_id": user_id})
            if existing:
                log.info(f"User {user_id} is already an admin.")
                return False
            
            if username:
                username = username.lower()
            else:
                username = None

            await cls.collection.insert_one({
                "user_id": user_id,
                "username": username,
                "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "promoted_by": promoted_by
            })

            log.info(f"Admin added successfully: {username or user_id} by {promoted_by}")
            return True

        except Exception as e:
            log.error(f"Error adding admin: {e}")
            return False

            
    @classmethod
    async def get_admin(cls , user_id : int):
        try:
            info_admin = await cls.collection.find_one({"user_id": user_id})
            return info_admin
        except Exception as e:
            log.error(f"Error getting admin: {e}")
       
    @classmethod     
    async def is_admin(cls, user_id: int):
        try:
            return await cls.collection.find_one({"user_id": user_id})
        except Exception as e:
            log.error(f"Error checking admin status: {e}")
            
    @classmethod
    async def get_all(cls):
        try:       
            cursor = cls.collection.find({})
            return [doc async for doc in cursor]
        except Exception as e:
            log.error(f"Error getting all admins: {e}")
    
    @classmethod
    async def remove_admin(cls, admin_id: int):
        try:
            return await cls.collection.delete_one({"user_id": admin_id})
            
        except Exception as e:
            log.error(f"Error removing admin: {e}")