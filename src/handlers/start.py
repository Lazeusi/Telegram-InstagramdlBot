from aiogram.filters import CommandStart 
from aiogram import Router, F , types

from src.logger import get_logger

log = get_logger()

router = Router()

@router.message(CommandStart())
async def start_handler(msg: types.Message ,bot):
    try:
        
            await msg.answer("Ok")
    except Exception as e:
        log.error(f"We got an error: {e}")

