from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from src.database.models.channels import Channel
from src.keyboards.inline.channel import list_channels_join_keyboard
from src.logger import get_logger

log = get_logger()

# حافظه موقت برای ذخیره هندلرهای منتظر
pending_users = {}

class ForceJoinMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        bot = data.get("bot")

        if isinstance(event, (Message, CallbackQuery)):
            user = event.from_user
            user_id = user.id

            # اگه خود دکمه "check_join" هست، اجازه بده اجرا بشه
            if isinstance(event, CallbackQuery) and event.data == "check_join":
                return await handler(event, data)

            # بررسی عضویت در کانال‌ها
            try:
                required_channels = await Channel.get_all()
                not_joined = []

                for ch in required_channels:
                    channel_id = int(ch["channel_id"])
                    try:
                        member = await bot.get_chat_member(channel_id, user_id)
                        if member.status in ("left", "kicked"):
                            not_joined.append(ch)
                    except Exception as e:
                        log.warning(f"Cannot check membership for {channel_id}: {e}")

                if not_joined:
                    keyboard = await list_channels_join_keyboard(not_joined)
                    text = "🚫 Please join all required channels to continue using the bot."

                    # ❌ ذخیره هندلر اصلی برای بعد از عضویت
                    pending_users[user_id] = (handler, event, data)

                    if isinstance(event, Message):
                        await event.answer(text, reply_markup=keyboard)
                    elif isinstance(event, CallbackQuery):
                        await event.message.edit_text(text, reply_markup=keyboard)
                        await event.answer()
                    return

            except Exception as e:
                log.error(f"ForceJoinMiddleware error: {e}")

        # در صورت عضویت کامل، ادامه بده
        return await handler(event, data)
