from aiogram.filters import Command
from aiogram import Router, F, types , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup , State
from datetime import datetime

from src.keyboards.inline.panel import (admin_keyboard , cancel_keyboard ,
                                        remove_admin_keyboard , accept_remove_admin_keyboard , 
                                        list_admin_keyboard , back_to_admin_list_keyboard ,
                                        back_to_admin_panel_keyboard)
from src.logger import get_logger
from src.database.models.admins import Admin
from src.database.models.users import User 
from src.config import settings


bot = Bot(token=settings.BOT_TOKEN)
log = get_logger()
router = Router()


@router.message(Command("activate"))
async def active_admin(msg: types.Message):
    try:
        exist = await Admin.get_all()
        if not exist:
            await Admin.add_admin(user_id=msg.from_user.id , username=msg.from_user.username)
            await msg.answer(f"شما به ربات دسترسی داده شدید")
        else:
            return
    except Exception as e:
        log.error(f"We got an error: {e}")
@router.message(Command("panel"))
async def admin_handler(msg: types.Message):
    try:
        if not await Admin.is_admin(user_id=msg.from_user.id):
            await msg.reply("شما ادمین نیستید")
            return
        await msg.answer(f"\n\n--------------پنل ادمین--------------\n\n",
                         reply_markup=await admin_keyboard()
                         )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
@router.callback_query(F.data == "close")
async def close_handler(call: types.CallbackQuery):
    try:      
        await call.message.edit_text(f"پنل ادمین بسته شد")
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")
   
class AdminStates(StatesGroup):
    wait_for_admin_username_or_id = State()


@router.callback_query(F.data == "add_admin")
async def add_admin_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            "لطفا نام کاربری یا شناسه کاربر را وارد کنید:\n\n",
            reply_markup=await cancel_keyboard()
        )
        await call.answer()
        await state.update_data(prompt_message_id = call.message.message_id)
        await state.set_state(AdminStates.wait_for_admin_username_or_id)
    except Exception as e:
        log.error(f"We got an error: {e}")


@router.callback_query(F.data == "cancel")
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            "شما برگشتید\n\n--------------پنل ادمین--------------\n\n",
            reply_markup=await admin_keyboard()
        )
        await call.answer()
        await state.clear()
    except Exception as e:
        log.error(f"We got an error: {e}")


@router.message(AdminStates.wait_for_admin_username_or_id)
async def process_admin_input(msg: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        prompt_message_id = data.get("prompt_message_id")
        await bot.delete_message(msg.from_user.id, prompt_message_id)
        text = msg.text.strip().lstrip("@")
        if text.isdigit():
            user = await User.get_user(user_id=int(text))
        else:
            user = await User.get_user(username=text.lower())

        if not user:
            await msg.answer("❌ کاربری با این شناسه یا نام کاربری یافت نشد." , reply_markup= await back_to_admin_panel_keyboard())
            return

        success = await Admin.add_admin(
            user_id=user["user_id"],
            username=user.get("username"),
            promoted_by=msg.from_user.username or msg.from_user.id
        )

        if success:
            uname = f"@{user.get('username')}" if user.get("username") else "No Username"
            await msg.answer(
                f"✅ ادمین با موفقیت اضافه شد\n"
                f"👤 Username: {uname}\n"
                f"🆔 User ID: {user['user_id']}\n"
                f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            await bot.send_message(user["user_id"], f" شما به ربات دسترسی داده شدید توسط {msg.from_user.first_name}.")
        else:
            await msg.answer("⚠️ کاربر از قبل ادمین بوده" , reply_markup= await back_to_admin_panel_keyboard())

        await state.clear()
    except Exception as e:
        log.error(f"We got an error: {e}")


@router.callback_query(F.data == "remove_admin")
async def remove_admin_handler(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "لطفا ادمینی که میخواهید حذف کنید را انتخاب کنید:\n\n",
            reply_markup=await remove_admin_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")
        
@router.callback_query(F.data == "back_to_admin_panel")
async def cancel_remove_admin_handler(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "شما برگشتید\n\n--------------پنل ادمین--------------\n\n",
            reply_markup=await admin_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")

@router.callback_query(F.data.startswith("remove_admin_"))
async def remove_admin(call: types.CallbackQuery, state: FSMContext):
    try:
        admin_id = int(call.data.split("_")[2])
        await call.message.edit_text(
            f"آیا مطمئن هستید که میخواهید ادمین با شناسه {admin_id} را حذف کنید؟\n\n",
            reply_markup=await accept_remove_admin_keyboard(admin_id)
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")

@router.callback_query(F.data.startswith("accept_remove_admin_"))
async def accept_remove_admin(call: types.CallbackQuery, state: FSMContext):
    try:
        admin_id = int(call.data.split("_")[3])
        await Admin.remove_admin(admin_id)
        await call.message.edit_text(
            f"ادمین با شناسه {admin_id} با موفقیت حذف شد",
            log.info(f"Admin with ID {admin_id} removed successfully by {call.from_user.first_name}"),
            reply_markup=await admin_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")
        
@router.callback_query(F.data == "admin_list")
async def remove_admin_handler(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "لیست ادمین ها:\n\n",
            reply_markup=await list_admin_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")

@router.callback_query(F.data.startswith("info_admin_"))
async def info_admin_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        admin_id = int(call.data.split("_")[2])
        admin = await Admin.get_admin(admin_id)
        await call.message.edit_text(
            f"👤 Username: @{admin.get('username')}\n"
            f"🆔 User ID: {admin['user_id']}\n"
            f"🕒 Set date: {admin['joined_at']}\n"
            f"🚀 Promoted by: @{admin['promoted_by']}" ,
            reply_markup=await back_to_admin_list_keyboard()
            
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")
        
@router.callback_query(F.data == "back_to_admin_list")
async def back_to_admin_list_handler(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "Admins list:",
            reply_markup=await list_admin_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")
        
        
class FindUserState(StatesGroup):
    wait_for_user_username_or_id = State()
@router.callback_query(F.data == "find_user")
async def find_user_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            "لطفا نام کاربری یا شناسه کاربر را وارد کنید:\n\n",
            reply_markup=await cancel_keyboard()
        )
        await call.answer()
        await state.update_data(prompt_message_id = call.message.message_id)
        await state.set_state(FindUserState.wait_for_user_username_or_id)
    except Exception as e:
        log.error(f"We got an error: {e}")
        
@router.message(FindUserState.wait_for_user_username_or_id)
async def find_user(message: types.Message, state: FSMContext):
    try:
        try:
            data = await state.get_data()
            prompt_message_id = data.get("prompt_message_id")
            await bot.delete_message(message.from_user.id, prompt_message_id)
        except Exception as e:
            log.warning(f"Failed to delete prompt message: {e}")

        if message.text.startswith("@"):
            user = await User.get_user(username=message.text[1:])
        else:
            user = await User.get_user(user_id=int(message.text))
        if user:
            await message.answer(
                f"👤 Username: @{user['username']}\n"
                f"🆔 User ID: {user['user_id']}\n"
                f"🕒 Join at: {user['joined_at']}\n" ,
                reply_markup= await back_to_admin_panel_keyboard()
            )
        else:
            await message.answer("❌ کاربری با این شناسه یا نام کاربری یافت نشد." ,
                                 reply_markup= await back_to_admin_panel_keyboard())
    except Exception as e:
        log.error(f"We got an error: {e}")