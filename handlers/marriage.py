from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import (
    register_user, get_partner, create_marriage, 
    delete_marriage, get_children
)
from keyboards import get_marry_keyboard, get_divorce_keyboard

router = Router()


@router.message(Command("marry"))
async def marry_command(message: Message):
    """Команда /marry - предложение о браке"""
    if not message.reply_to_message:
        await message.reply("❌ Используйте эту команду реплаем на человека!")
        return
    
    user1_id = message.from_user.id
    user2_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    # Регистрация пользователей
    await register_user(user1_id, chat_id, message.from_user.first_name)
    await register_user(user2_id, chat_id, message.reply_to_message.from_user.first_name)
    
    # Проверки
    if user1_id == user2_id:
        await message.reply("❌ Нельзя жениться на себе!")
        return
    
    if message.reply_to_message.from_user.is_bot:
        await message.reply("❌ Нельзя жениться на боте!")
        return
    
    partner = await get_partner(user1_id, chat_id)
    if partner:
        await message.reply("❌ Вы уже в браке!")
        return
    
    partner2 = await get_partner(user2_id, chat_id)
    if partner2:
        await message.reply("❌ Этот пользователь уже в браке!")
        return
    
    # Отправка предложения
    await message.reply(
        f"💍 {message.from_user.first_name} делает предложение {message.reply_to_message.from_user.first_name}!",
        reply_markup=get_marry_keyboard(user1_id, user2_id)
    )


@router.callback_query(F.data.startswith("marry_accept:"))
async def marry_accept(callback: CallbackQuery):
    """Принятие предложения о браке"""
    _, user1_id, user2_id = callback.data.split(":")
    user1_id = int(user1_id)
    user2_id = int(user2_id)
    
    if callback.from_user.id != user2_id:
        await callback.answer("❌ Это не ваше предложение!", show_alert=True)
        return
    
    chat_id = callback.message.chat.id
    
    # Повторная проверка браков
    partner1 = await get_partner(user1_id, chat_id)
    partner2 = await get_partner(user2_id, chat_id)
    
    if partner1 or partner2:
        await callback.message.edit_text("❌ Кто-то из вас уже успел пожениться!")
        await callback.answer()
        return
    
    await create_marriage(user1_id, user2_id, chat_id)
    await callback.message.edit_text(
        f"💒 Поздравляем! Теперь вы в браке! 🎉"
    )
    await callback.answer("✅ Вы приняли предложение!")


@router.callback_query(F.data.startswith("marry_decline:"))
async def marry_decline(callback: CallbackQuery):
    """Отклонение предложения о браке"""
    _, user1_id, user2_id = callback.data.split(":")
    user2_id = int(user2_id)
    
    if callback.from_user.id != user2_id:
        await callback.answer("❌ Это не ваше предложение!", show_alert=True)
        return
    
    await callback.message.edit_text("💔 Предложение отклонено.")
    await callback.answer("❌ Вы отклонили предложение")


@router.message(Command("divorce"))
async def divorce_command(message: Message):
    """Команда /divorce - развод"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    await register_user(user_id, chat_id, message.from_user.first_name)
    
    partner = await get_partner(user_id, chat_id)
    if not partner:
        await message.reply("❌ Вы не в браке!")
        return
    
    await message.reply(
        f"💔 Вы уверены, что хотите развестись с {partner['first_name']}?",
        reply_markup=get_divorce_keyboard(user_id)
    )


@router.callback_query(F.data.startswith("divorce_confirm:"))
async def divorce_confirm(callback: CallbackQuery):
    """Подтверждение развода"""
    user_id = int(callback.data.split(":")[1])
    
    if callback.from_user.id != user_id:
        await callback.answer("❌ Это не ваш развод!", show_alert=True)
        return
    
    chat_id = callback.message.chat.id
    partner = await get_partner(user_id, chat_id)
    
    if not partner:
        await callback.message.edit_text("❌ Вы не в браке!")
        await callback.answer()
        return
    
    await delete_marriage(user_id, chat_id)
    await callback.message.edit_text(
        f"💔 Развод оформлен. {callback.from_user.first_name} и {partner['first_name']} больше не в браке."
    )
    await callback.answer("✅ Развод оформлен")


@router.callback_query(F.data.startswith("divorce_cancel:"))
async def divorce_cancel(callback: CallbackQuery):
    """Отмена развода"""
    user_id = int(callback.data.split(":")[1])
    
    if callback.from_user.id != user_id:
        await callback.answer("❌ Это не ваш развод!", show_alert=True)
        return
    
    await callback.message.edit_text("❤️ Развод отменён. Любовь победила!")
    await callback.answer("✅ Отменено")
