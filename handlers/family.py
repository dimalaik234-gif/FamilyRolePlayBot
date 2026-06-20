from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import (
    register_user, adopt_child, disown_child,
    get_children, get_parents, has_parent, get_partner
)
# ИЗМЕНЕНО: прямой импорт из keyboards.inline
from keyboards.inline import get_adopt_keyboard, get_disown_keyboard

router = Router()

# ... остальной код без изменений
