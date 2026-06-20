from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import register_user, set_role
# ИЗМЕНЕНО: прямой импорт из keyboards.inline
from keyboards.inline import get_roles_keyboard

router = Router()

# ... остальной код без изменений


@router.message(Command("setrole"))
async def setrole_command(message: Message):
    """Команда /setrole - выбрать роль"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    await register_user(user_id, chat_id, message.from_user.first_name)
    
    await message.reply(
        "🎭 <b>Выберите роль:</b>",
        reply_markup=get_roles_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("role:"))
async def role_select(callback: CallbackQuery):
    """Выбор роли"""
    role = callback.data.split(":")[1]
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    
    if role == "reset":
        await set_role(user_id, chat_id, None)
        await callback.message.edit_text("✅ Роль сброшена!")
    else:
        await set_role(user_id, chat_id, role)
        await callback.message.edit_text(f"✅ Ваша роль теперь: <b>{role}</b>", parse_mode="HTML")
    
    await callback.answer()
