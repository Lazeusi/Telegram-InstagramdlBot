from aiogram import Router, types, F
from src.middleware.force_join import pending_users
from src.database.models.channels import Channel
from src.keyboards.inline.channel import list_channels_join_keyboard
from src.logger import get_logger

log = get_logger()
router = Router()

@router.callback_query(F.data == "check_join")
async def check_join_handler(call: types.CallbackQuery, bot):
    user_id = call.from_user.id
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
        await call.message.edit_text(
            "🚫 شما هنوز عضو تمام کانال ها نشدید",
            reply_markup=keyboard
        )
        await call.answer()
        return

    # ✅ کاربر حالا عضو شده
    await call.message.edit_text("✅ شما با موفقیت عضو شدید")
    await call.answer()

    # 🧠 ادامه هندلر اصلی (Resume)
    if user_id in pending_users:
        handler, event, data = pending_users.pop(user_id)
        try:
            await handler(event, data)  # 🔥 ادامه همون کاری که قبل از force join قطع شده بود
        except Exception as e:
            log.error(f"Failed to resume handler for {user_id}: {e}")
