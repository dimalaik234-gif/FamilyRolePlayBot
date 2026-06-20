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
    text = f"╔═══════════════════════╗\n"
    text += f"👨‍👩‍👧‍👦 <b>Семья {message.from_user.first_name}</b>\n"
    text += f"╚═══════════════════════╝\n\n"
    
    if partner:
        role = f" 🎭 {partner['role']}" if partner['role'] else ""
        text += f"💑 <b>Супруг(а):</b>\n"
        text += f"   └ {partner['first_name']}{role}\n\n"
    else:
        text += "💑 <b>Супруг(а):</b> <i>нет</i>\n\n"
    
    if children:
        text += f"👶 <b>Дети ({len(children)}):</b>\n"
        for i, child in enumerate(children, 1):
            role = f" 🎭 {child['role']}" if child['role'] else ""
            prefix = "├" if i < len(children) else "└"
            text += f"   {prefix} {child['first_name']}{role}\n"
        text += "\n"
    else:
        text += "👶 <b>Дети:</b> <i>нет</i>\n\n"
    
    if parents:
        text += f"👨 <b>Родители ({len(parents)}):</b>\n"
        for i, parent in enumerate(parents, 1):
            role = f" 🎭 {parent['role']}" if parent['role'] else ""
            prefix = "├" if i < len(parents) else "└"
            text += f"   {prefix} {parent['first_name']}{role}\n"
    else:
        text += "👨 <b>Родители:</b> <i>нет</i>"
    
    await message.reply(text, parse_mode="HTML")
