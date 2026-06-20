from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_marry_keyboard(user1_id: int, user2_id: int):
    """Кнопка подтверждения брака"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Принять предложение",
                callback_data=f"marry_accept:{user1_id}:{user2_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"marry_decline:{user1_id}:{user2_id}"
            )
        ]
    ])


def get_divorce_keyboard(user_id: int):
    """Кнопка подтверждения развода"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Да, развестись",
                callback_data=f"divorce_confirm:{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data=f"divorce_cancel:{user_id}"
            )
        ]
    ])


def get_adopt_keyboard(parent_id: int, child_id: int):
    """Кнопка подтверждения усыновления"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Согласиться",
                callback_data=f"adopt_accept:{parent_id}:{child_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отказаться",
                callback_data=f"adopt_decline:{parent_id}:{child_id}"
            )
        ]
    ])


def get_disown_keyboard(parent_id: int, child_id: int):
    """Кнопка подтверждения отказа от ребёнка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Да, отказаться",
                callback_data=f"disown_confirm:{parent_id}:{child_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data=f"disown_cancel:{parent_id}:{child_id}"
            )
        ]
    ])


def get_roles_keyboard():
    """Клавиатура выбора роли"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 Лупа", callback_data="role:Лупа")],
        [InlineKeyboardButton(text="🟡 Пупа", callback_data="role:Пупа")],
        [InlineKeyboardButton(text="🟣 Залупа", callback_data="role:Залупа")],
        [InlineKeyboardButton(text="🦸 Залупомэн", callback_data="role:Залупомэн")],
        [InlineKeyboardButton(text="❌ Сбросить роль", callback_data="role:reset")]
    ])
