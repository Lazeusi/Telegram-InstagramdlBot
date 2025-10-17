from aiogram.filters import Command
from aiogram import F , Router , types , Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.database.models.channels import Channel
from src.logger import get_logger
from src.keyboards.inline.panel import back_to_admin_panel_keyboard  
from src.keyboards.inline.channel import( channel_keyboard , back_to_force_join_panel_keyboard ,
                                        confirm_add_force_channel_keyboard  , ch_remove_keyboard ,
                                        accept_remove_channel_keyboard , list_channels_keyboard ,
                                        back_to_channel_list )
from src.config import settings


bot = Bot(token=settings.BOT_TOKEN)

router = Router()

log = get_logger()

@router.callback_query(F.data == "force_join")
async def channel_list_handler(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "پنل جوین اجباری:\n\n",
            reply_markup=await channel_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")
        
class ForceJoinState(StatesGroup):
    wait_for_chat = State()


class ForceJoinState(StatesGroup):
    wait_for_chat = State()
    confirm_chat = State()


@router.callback_query(F.data == "add_channel")
async def ask_for_chat(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            "📢 لطفا طبق یکی از مراحل پیش برید.\n"
            "1️⃣ برای گروه یا کانال های عمومی فقط @username را وارد کنید\n"
            "2️⃣ برای کانال های خصوصی یک پیام از آن کانال را فوروارد کنید\n\n",
            reply_markup=await back_to_force_join_panel_keyboard()
        )
        await state.update_data(prompt_message_id=call.message.message_id)
        await state.set_state(ForceJoinState.wait_for_chat)
        await call.answer()
    except Exception as e:
        log.error(f"We got an error: {e}")


@router.message(ForceJoinState.wait_for_chat)
async def get_chat_id(message: types.Message, state: FSMContext):
    try:
        try:
            data = await state.get_data()
            prompt_message_id = data.get("prompt_message_id")
            await bot.delete_message(message.from_user.id, prompt_message_id)
        except Exception as e:
            log.warning(f"Failed to delete prompt message: {e}")
            
            
        chat_id = None
        title = None

        # Option 1: Forwarded message (private chat)
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            title = message.forward_from_chat.title

        # Option 2: Public chat via @username
        elif message.text and message.text.startswith("@"):
            chat = await message.bot.get_chat(message.text)
            chat_id = chat.id
            title = chat.title

        else:
            await message.answer(
                "⚠️ لطفا یک گروه یا کانال عمومی را وارد کنید یا پیامی از آن کانال را فوروارد کنید.",
                reply_markup=await back_to_force_join_panel_keyboard()
            )
            return

        # Save temporarily in FSM context
        await state.update_data(chat_id=chat_id, title=title)


        await message.answer(
            f"📛 Title: {title}\n"
            f"🆔 Chat ID: <code>{chat_id}</code>\n\n"
            f"آیا مطمئن هستید که میخواهید این کانال را به لیست جوین اجباری اضافه کنید؟",
            parse_mode="HTML",
            reply_markup= await confirm_add_force_channel_keyboard()
        )

        await state.set_state(ForceJoinState.confirm_chat)

    except TelegramBadRequest:
        await message.answer(
            "❌ Failed to find the chat. Make sure the bot is a member of that chat.",
            reply_markup=await back_to_admin_panel_keyboard()
        )
    except Exception as e:
        await message.answer(
            f"⚠️ خطایی به وجود آمده: {e}",
            reply_markup=await back_to_admin_panel_keyboard()
        )


@router.callback_query(F.data == "confirm_add")
async def confirm_chat(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        chat_id = data.get("chat_id")
        title = data.get("title")
        
        await Channel.add_channel(chat_id, title)
    except Exception as e:
        log.error(f"We got an error: {e}")


    await call.message.edit_text(
        f"✅ کانال با موفقیت به لیست جوین اجباری اضافه شد\n\n"
        f"📛 Title: {title}\n"
        f"🆔 Chat ID: <code>{chat_id}</code>",
        parse_mode="HTML",
        reply_markup=await back_to_admin_panel_keyboard()
    )
    log.info(f"Channel {title} was added")
    await state.clear()
    await call.answer()


@router.callback_query(F.data == "remove_channel")
async def remove_channel(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "لطفا کانالی که میخواهید حذف کنید را انتخاب کنید",
            reply_markup=await ch_remove_keyboard()
        )
    except Exception as e:
        log.error(f"Error removing channel: {e}")
    

@router.callback_query(F.data.startswith("remove_channel_"))
async def input_channel(call: types.CallbackQuery , state: FSMContext):
    try:
        chat_id = int(call.data.split("_")[2])     
        info = await Channel.get_channel(chat_id)
        await state.update_data(chat_id=chat_id , info=info)
        await call.message.edit_text(
            f"شما در حال حذف کانال زیر هستید\n\n"
            f"📛 Title: {info['title']}\n"
            f"🆔 Chat ID: <code>{info['channel_id']}</code>\n\n"
            f"آیا مطمئن هستید که میخواهید این کانال را حذف کنید؟",
            parse_mode="HTML" ,          
            reply_markup=await accept_remove_channel_keyboard()
        )
        await call.answer()
        
    except Exception as e:
        log.error(f"Error removing channel: {e}")
        
@router.callback_query(F.data == "confirm_remove")
async def remove_channel(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        chat_id = data.get("chat_id")
        info = data.get("info")
        await Channel.remove_channel(chat_id)
        await call.message.edit_text(
            f"کانال {info['title']} با موفقیت حذف شد\n" ,
            reply_markup=await back_to_admin_panel_keyboard()
        )
        log.info(f"Channel {info['title']} was removed")
        await call.answer()
    except Exception as e:
        log.error(f"Error removing channel: {e}")
        
        
@router.callback_query(F.data == "channel_list")
async def channel_list(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "لیست کانال ها:",
            reply_markup=await list_channels_keyboard()
        )
        await call.answer()
    except Exception as e:
        log.error(f"Error listing channels: {e}")
        
@router.callback_query(F.data.startswith("info_channel_"))
async def info_channel(call: types.CallbackQuery):
    try:
        chat_id = int(call.data.split("_")[2])
        info = await Channel.get_channel(chat_id)
        await call.message.edit_text(
            f"📢 اطلاعات کانال/گروه \n\n"
            f"📛 Title: {info['title']}\n"
            f"🆔 Chat ID: <code>{info['channel_id']}</code>\n"
            f"🕝 Aded at: {info['added_at']}",
            parse_mode="HTML" ,
            reply_markup= await back_to_channel_list()
        )
        await call.answer()
    except Exception as e:
        log.error(f"Error listing channels: {e}")