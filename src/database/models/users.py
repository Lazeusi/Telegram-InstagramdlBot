from src.database.connection import db
from src.logger import get_logger


from datetime import datetime

log = get_logger()

class User:

    collection = db.users
    

    @classmethod
    async def add_user(cls , user_id , username : str = None):
        try:
            if username:
                username = username.lower()
            await cls.collection.insert_one({                                  
                                    "user_id" : user_id,
                                    "username" : username , # username
                                    "joined_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,
            })
        except Exception as e:
            log.error(f"Error adding user: {e}")
    
    @classmethod
    async def get_user(cls , user_id : int = None, username : str = None):
        try:
            
                
            if user_id:
                return await cls.collection.find_one({"user_id" : user_id})
            if username:
                username = username.lower()
                return await cls.collection.find_one({"username" : username })
        except Exception as e:
            log.error(f"Error getting user: {e}")

    @classmethod
    async def get_all_users(cls):
        try:
            return await cls.collection.find()
        except Exception as e:
            log.error(f"Error getting all users: {e}")
            
    @classmethod
    async def update_user(cls , user_id : int , username : str = None):
        try:
            if username:
                username = username.lower()
                return cls.collection.update_one({"user_id" : user_id} , {"$set" : {"username" : username}})
        except Exception as e:
            log.error(f"Error updating user: {e}")
            