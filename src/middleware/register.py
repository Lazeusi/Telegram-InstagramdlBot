from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime

from src.logger import get_logger
from src.database.models.users import User


log = get_logger()



class RegisterMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
                       event: Any,
                       data: Dict[str, Any]) -> Any:

        if hasattr(event, "from_user") and event.from_user:
            user_id = event.from_user.id
            username = event.from_user.username
           
            # if user_id and username:
            existing_user = await User.get_user(user_id=user_id)
            if not existing_user:
                await User.add_user(user_id=user_id, username=username)
                log.info(f"New user added, Username: @{username.lower()}, User ID: {user_id}, Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                await User.update_user(user_id=user_id , username=username)
                log.info(f"User @{username.lower()} was used bot, User ID: {user_id}, Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                
            
        # after doing the job, go to the main handler
        return await handler(event, data)
            
            
