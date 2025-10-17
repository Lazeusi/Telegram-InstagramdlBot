from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramNetworkError
import asyncio

from src.config import settings
from src.handlers import setup_handlers
from src.middleware import setup_middlewares
from src.logger import get_logger
from src.database.connection import db



log = get_logger()
async def main():
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    await db.connect()
    
    # middlewares
    setup_middlewares(dp)
    
    # handlers
    setup_handlers(dp)
    
    log.info("Bot is polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except TelegramNetworkError as e:
        log.warning("Bot disconnected from Telegram servers. Reason: ", e)
  
    except (KeyboardInterrupt, SystemExit ):
        log.info("Bot disconnected. Shutting down...")
         
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        