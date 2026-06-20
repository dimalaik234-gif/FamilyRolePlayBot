from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import (
    register_user, adopt_child, disown_child,
    get_children, get_parents, has_parent, get_partner
)
from keyboards import get_adopt_keyboard, get_disown_keyboard

router = Router()


@router.message(Command("adopt"))
async def adopt_command(message: Message):
    """Команда /adopt - усыновить"""
    if not message.reply_to_message:
        await message.reply("❌ Используйте эту команду реплаем на человека!")
        return
    
    parent_id = message.from_user.id
    child_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    await register_user(parent_id, chat_id, message.from_user.first_name)
    await register_user(child_id, chat_id, message.reply_to_message.from_user.first_name)
    
    # Проверки
    if parent_id == child_id:
        await message.reply("❌ Нельзя усыновить себя!")
        return
    
    if message.reply_to_message.from_user.is_bot:
        await message.reply("❌ Нельзя усыновить бота!")
        return
    
    # Проверка, не является ли пользователь уже ребёнком
    children = await get_children(parent_id, chat_id)
    if any(c['user_id'] == child_id for c in children):
        await message.reply("❌ Этот пользователь уже ваш ребёнок!")
        return
    
    await message.reply(
        f"👶 {message.from_user.first_name} хочет усыновить {message.reply_to_message.from_user.first_name}!",
        reply_markup=get_adopt_keyboard(parent_id, child_id)
    )


@router.callback_query(F.data.startswith("adopt_accept:"))
async def adopt_accept(callback: CallbackQuery):
    """Принятие усыновления"""
    _, parent_id, child_id = callback.data.split(":")
    parent_id = int(parent_id)
    child_id = int(child_id)
    
    if callback.from_user.id != child_id:
        await callback.answer("❌ Это не вас усыновляют!", show_alert=True)
        return
    
    chat_id = callback.message.chat.id
    await adopt_child(parent_id, child_id, chat_id)
    
    await callback.message.edit_text(
        f"👨‍👩‍👧 Теперь вы семья! 🎉"
    )
    await callback.answer("✅ Вы согласились!")


@router.callback_query(F.data.startswith("adopt_decline:"))
async def adopt_decline(callback: CallbackQuery):
    """Отклонение усыновления"""
    _, parent_id, child_id = callback.data.split(":")
    child_id = int(child_id)
    
    if callback.from_user.id != child_id:
        await callback.answer("❌ Это не вас усыновляют!", show_alert=True)
        return
    
    await callback.message.edit_text("❌ Усыновление отклонено.")
    await callback.answer("❌ Вы отказались")


@router.message(Command("disown"))
async def disown_command(message: Message):
    """Команда /disown - отказаться от ребёнка"""
    if not message.reply_to_message:
        await message.reply("❌ Используйте эту команду реплаем на ребёнка!")
        return
    
    parent_id = message.from_user.id
    child_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    await register_user(parent_id, chat_id, message.from_user.first_name)
    
    children = await get_children(parent_id, chat_id)
    if not any(c['user_id'] == child_id for c in children):
        await message.reply("❌ Этот пользователь не ваш ребёнок!")
        return
    
    await message.reply(
        f"💔 Вы уверены, что хотите отказаться от {message.reply_to_message.from_user.first_name}?",
        reply_markup=get_disown_keyboard(parent_id, child_id)
    )


@router.callback_query(F.data.startswith("disown_confirm:"))
async def disown_confirm(callback: CallbackQuery):
    """Подтверждение отказа от ребёнка"""
    _, parent_id, child_id = callback.data.split(":")
    parent_id = int(parent_id)
    child_id = int(child_id)
    
    if callback.from_user.id != parent_id:
        await callback.answer("❌ Это не ваш ребёнок!", show_alert=True)
        return
    
    chat_id = callback.message.chat.id
    await disown_child(parent_id, child_id, chat_id)
    
    await callback.message.edit_text("💔 Вы отказались от ребёнка.")
    await callback.answer("✅ Отказ оформлен")


@router.callback_query(F.data.startswith("disown_cancel:"))
async def disown_cancel(callback: CallbackQuery):
    """Отмена отказа от ребёнка"""
    parent_id = int(callback.data.split(":")[1])
    
    if callback.from_user.id != parent_id:
        await callback.answer("❌ Это не ваш ребёнок!", show_alert=True)
        return
    
    await callback.message.edit_text("❤️ Отказ отменён. Семья важнее!")
    await callback.answer("✅ Отменено")


@router.message(Command("family"))
async def family_command(message: Message):
    """Команда /family - показать семью"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    await register_user(user_id, chat_id, message.from_user.first_name)
    
    # Получаем данные
    partner = await get_partner(user_id, chat_id)
    children = await get_children(user_id, chat_id)
    parents = await get_parents(user_id, chat_id)
    
    # Формируем текст
    text = f"👨‍👩‍👧‍👦 <b>Семья {message.from_user.first_name}</b>\n\n"
    
    if partner:
        role = f" ({partner['role']})" if partner['role'] else ""
        text += f"💑 <b>Супруг(а):</b> {partner['first_name']}{role}\n\n"
    else:
        text += "💑 <b>Супруг(а):</b> нет\n\n"
    
    if children:
        text += "👶 <b>Дети:</b>\n"
        for child in children:
            role = f" ({child['role']})" if child['role'] else ""
            text += f"  • {child['first_name']}{role}\n"
        text += "\n"
    else:
        text += "👶 <b>Дети:</b> нет\n\n"
    
    if parents:
        text += "👨 <b>Родители:</b>\n"
        for parent in parents:
            role = f" ({parent['role']})" if parent['role'] else ""
            text += f"  • {parent['first_name']}{role}\n"
    else:
        text += "👨 <b>Родители:</b> нет"
    
    await message.reply(text, parse_mode="HTML")
