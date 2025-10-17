from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logger import get_logger
from src.database.models.admins import Admin

log = get_logger()


async def admin_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Add admin", callback_data="add_admin") , InlineKeyboardButton(text="Remove admin", callback_data="remove_admin")],
                [InlineKeyboardButton(text="Admin list", callback_data="admin_list")],
                [InlineKeyboardButton(text="Find user", callback_data="find_user") , InlineKeyboardButton(text="Force join", callback_data="force_join")],
                [InlineKeyboardButton(text="Close", callback_data="close")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def cancel_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Cancel", callback_data="cancel")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def remove_admin_keyboard():
    try:
        builder = InlineKeyboardBuilder()
        admins = await Admin.get_all()

        if not admins:
            builder.button(text="❌ No admins found", callback_data="none")
            return builder.as_markup()

        for admin in admins:
            uname = f"@{admin['username']}" if admin.get("username") else str(admin["user_id"])
            builder.button(
                text=f"🧑 {uname}",
                callback_data=f"remove_admin_{admin['user_id']}"
            )

        builder.button(text="Back", callback_data="back_to_admin_panel")

        builder.adjust(1)  
        return builder.as_markup()

    except Exception as e:
        log.error(f"We got an error: {e}")

async def accept_remove_admin_keyboard(admin_id: int):
    try:
        builder = InlineKeyboardBuilder()
        builder.button(text="Yes", callback_data=f"accept_remove_admin_{admin_id}")
        builder.button(text="No", callback_data="back_to_admin_panel")
        return builder.as_markup()
    except Exception as e:
        log.error(f"We got an error: {e}")

async def list_admin_keyboard():
    try:
        builder = InlineKeyboardBuilder()
        admins = await Admin.get_all()

        if not admins:
            builder.button(text="❌ No admins found", callback_data="none")
            return builder.as_markup()

        for admin in admins:
            uname = f"@{admin['username']}" if admin.get("username") else str(admin["user_id"])
            builder.button(
                text=f"😎🤞 {uname}",
                callback_data=f"info_admin_{admin['user_id']}"
            )

        builder.button(text="Back", callback_data="back_to_admin_panel")

        builder.adjust(1) 
        return builder.as_markup()

    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def back_to_admin_list_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_admin_list")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def back_to_admin_panel_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_admin_panel")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
