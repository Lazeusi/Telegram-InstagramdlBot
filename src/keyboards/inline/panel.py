from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logger import get_logger
from src.database.models.admins import Admin

log = get_logger()


async def admin_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="اضافه کردن ادمین", callback_data="add_admin") , InlineKeyboardButton(text="حذف کردن ادمین", callback_data="remove_admin")],
                [InlineKeyboardButton(text="لیست ادمین ها", callback_data="admin_list")],
                [InlineKeyboardButton(text="پیدا کردن کاربر", callback_data="find_user") , InlineKeyboardButton(text="جوین اجباری", callback_data="force_join")],
                [InlineKeyboardButton(text="بستن", callback_data="close")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def cancel_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="لغو", callback_data="cancel")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def remove_admin_keyboard():
    try:
        builder = InlineKeyboardBuilder()
        admins = await Admin.get_all()

        if not admins:
            builder.button(text="هیچ ادمینی یافت نشد", callback_data="none")
            return builder.as_markup()

        for admin in admins:
            uname = f"@{admin['username']}" if admin.get("username") else str(admin["user_id"])
            builder.button(
                text=f"🧑 {uname}",
                callback_data=f"remove_admin_{admin['user_id']}"
            )

        builder.button(text="برگشت", callback_data="back_to_admin_panel")

        builder.adjust(1)  
        return builder.as_markup()

    except Exception as e:
        log.error(f"We got an error: {e}")

async def accept_remove_admin_keyboard(admin_id: int):
    try:
        builder = InlineKeyboardBuilder()
        builder.button(text="تایید", callback_data=f"accept_remove_admin_{admin_id}")
        builder.button(text="لغو", callback_data="back_to_admin_panel")
        return builder.as_markup()
    except Exception as e:
        log.error(f"We got an error: {e}")

async def list_admin_keyboard():
    try:
        builder = InlineKeyboardBuilder()
        admins = await Admin.get_all()

        if not admins:
            builder.button(text="هیچ ادمینی یافت نشد", callback_data="none")
            return builder.as_markup()

        for admin in admins:
            uname = f"@{admin['username']}" if admin.get("username") else str(admin["user_id"])
            builder.button(
                text=f"🧑 {uname}",
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
                [InlineKeyboardButton(text="🔙 برگشت", callback_data="back_to_admin_list")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def back_to_admin_panel_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 برگشت", callback_data="back_to_admin_panel")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
