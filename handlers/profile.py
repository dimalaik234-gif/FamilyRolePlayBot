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
    text = f"╔═══════════════════╗\n"
    text += f"👤 <b>{user['first_name']}</b>\n"
    text += f"╚═══════════════════╝\n\n"
    
    if user['role']:
        text += f"🎭 <b>Роль:</b> {user['role']}\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━\n\n"
    
    if partner:
        partner_role = f" ({partner['role']})" if partner['role'] else ""
        text += f"💑 <b>Партнёр:</b> {partner['first_name']}{partner_role}\n"
    else:
        text += f"💑 <b>Партнёр:</b> <i>свободен</i>\n"
    
    if children:
        text += f"👶 <b>Детей:</b> {len(children)}\n"
    else:
        text += f"👶 <b>Детей:</b> <i>нет</i>\n"
    
    if parents:
        text += f"👨 <b>Родителей:</b> {len(parents)}\n"
    else:
        text += f"👨 <b>Родителей:</b> <i>нет</i>\n"
    
    text += f"\n📅 <b>В семейке с:</b> {reg_date}"
    
    await message.reply(text, parse_mode="HTML")


@router.message(Command("stats"))
async def stats_command(message: Message):
    """Статистика чата"""
    if message.chat.type == "private":
        await message.reply("❌ Эта команда работает только в группах!")
        return
    
    chat_id = message.chat.id
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Всего пользователей
        async with db.execute(
            'SELECT COUNT(*) FROM users WHERE chat_id = ?', (chat_id,)
        ) as cursor:
            total_users = (await cursor.fetchone())[0]
        
        # Всего браков
        async with db.execute(
            'SELECT COUNT(*) FROM marriages WHERE chat_id = ?', (chat_id,)
        ) as cursor:
            total_marriages = (await cursor.fetchone())[0]
        
        # Всего детей
        async with db.execute(
            'SELECT COUNT(*) FROM children WHERE chat_id = ?', (chat_id,)
        ) as cursor:
            total_children = (await cursor.fetchone())[0]
        
        # Пользователи с ролями
        async with db.execute(
            'SELECT COUNT(*) FROM users WHERE chat_id = ? AND role IS NOT NULL', (chat_id,)
        ) as cursor:
            users_with_roles = (await cursor.fetchone())[0]
    
    text = f"""
╔═══════════════════════╗
  📊 <b>Статистика чата</b>
╚═══════════════════════╝

👥 <b>Всего участников:</b> {total_users}
💑 <b>Браков заключено:</b> {total_marriages}
👶 <b>Детей усыновлено:</b> {total_children}
🎭 <b>Пользователей с ролями:</b> {users_with_roles}

━━━━━━━━━━━━━━━━━━━━━
💡 <i>Статистика обновляется в реальном времени</i>
    """
    
    await message.reply(text.strip(), parse_mode="HTML")

@router.message(Command("help"))
async def help_command(message: Message):
    """Команда /help - список команд"""
    text = """
╔═══════════════════════╗
  📖 <b>Family RP Bot</b>
╚═══════════════════════╝

<b>💍 БРАК:</b>
/marry — предложить брак (реплаем)
/divorce — развестись

<b>👨‍👩‍👧‍👦 СЕМЬЯ:</b>
/adopt — усыновить (реплаем)
/disown — отказаться от ребёнка (реплаем)
/family — показать дерево семьи

<b>🎭 РОЛИ:</b>
/setrole — выбрать роль
<i>Доступны: Лупа, Пупа, Залупа, Залупомэн</i>

<b>👤 ПРОФИЛЬ:</b>
/profile — показать профиль
/help — список команд

━━━━━━━━━━━━━━━━━━━━━
💡 <i>Все команды работают в групповых чатах!</i>
    """
    await message.reply(text.strip(), parse_mode="HTML")


@router.message(Command("start"))
async def start_command(message: Message):
    """Команда /start"""
    if message.chat.type == "private":
        text = """
👋 <b>Привет! Я Family RP Bot!</b>

Добавь меня в групповой чат, чтобы:
💍 Жениться на друзьях
👶 Усыновлять участников
🎭 Выбирать прикольные роли
👨‍👩‍👧‍👦 Строить семейное древо

━━━━━━━━━━━━━━━━━━━━━
📖 Используй /help для списка команд
        """
        await message.reply(text.strip(), parse_mode="HTML")
    else:
        await help_command(message)
