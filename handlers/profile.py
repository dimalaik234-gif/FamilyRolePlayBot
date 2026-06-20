from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database import (
    register_user, get_user, get_partner,
    get_children, get_parents
)
from datetime import datetime

router = Router()


@router.message(Command("profile"))
async def profile_command(message: Message):
    """Команда /profile - показать профиль"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    await register_user(user_id, chat_id, message.from_user.first_name)
    
    user = await get_user(user_id, chat_id)
    partner = await get_partner(user_id, chat_id)
    children = await get_children(user_id, chat_id)
    parents = await get_parents(user_id, chat_id)
    
    # Форматируем дату
    reg_date = datetime.fromisoformat(user['registered_at']).strftime("%d.%m.%Y")
    
    # Формируем текст
    text = f"👤 <b>Профиль: {user['first_name']}</b>\n\n"
    
    if user['role']:
        text += f"🎭 <b>Роль:</b> {user['role']}\n\n"
    
    if partner:
        text += f"💑 <b>Партнёр:</b> {partner['first_name']}\n"
    
    if children:
        text += f"👶 <b>Детей:</b> {len(children)}\n"
    
    if parents:
        text += f"👨 <b>Родителей:</b> {len(parents)}\n"
    
    text += f"\n📅 <b>Зарегистрирован:</b> {reg_date}"
    
    await message.reply(text, parse_mode="HTML")


@router.message(Command("help"))
async def help_command(message: Message):
    """Команда /help - список команд"""
    text = """
📖 <b>Список команд бота:</b>

<b>💍 Брак:</b>
/marry — предложить брак (реплаем)
/divorce — развестись

<b>👨‍👩‍👧‍👦 Семья:</b>
/adopt — усыновить (реплаем)
/disown — отказаться от ребёнка (реплаем)
/family — показать дерево семьи

<b>🎭 Роли:</b>
/setrole — выбрать роль

<b>👤 Профиль:</b>
/profile — показать профиль

<b>📖 Помощь:</b>
/help — список команд
    """
    await message.reply(text.strip(), parse_mode="HTML")


@router.message(Command("start"))
async def start_command(message: Message):
    """Команда /start"""
    await help_command(message)
