import aiosqlite
from config import DB_PATH
from datetime import datetime


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                chat_id INTEGER,
                first_name TEXT,
                role TEXT DEFAULT NULL,
                registered_at TEXT,
                PRIMARY KEY (user_id, chat_id)
            )
        ''')
        
        # Таблица браков
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marriages (
                user1_id INTEGER,
                user2_id INTEGER,
                chat_id INTEGER,
                married_at TEXT,
                PRIMARY KEY (user1_id, user2_id, chat_id)
            )
        ''')
        
        # Таблица детей (parent_id - родитель, child_id - ребёнок)
        await db.execute('''
            CREATE TABLE IF NOT EXISTS children (
                parent_id INTEGER,
                child_id INTEGER,
                chat_id INTEGER,
                adopted_at TEXT,
                PRIMARY KEY (parent_id, child_id, chat_id)
            )
        ''')
        
        await db.commit()


async def register_user(user_id: int, chat_id: int, first_name: str):
    """Регистрация пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, chat_id, first_name, registered_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, chat_id, first_name, datetime.now().isoformat()))
        await db.commit()


async def get_user(user_id: int, chat_id: int):
    """Получить данные пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT * FROM users WHERE user_id = ? AND chat_id = ?
        ''', (user_id, chat_id)) as cursor:
            return await cursor.fetchone()


async def set_role(user_id: int, chat_id: int, role: str = None):
    """Установить роль пользователю"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            UPDATE users SET role = ? WHERE user_id = ? AND chat_id = ?
        ''', (role, user_id, chat_id))
        await db.commit()


async def get_partner(user_id: int, chat_id: int):
    """Получить партнёра"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT user1_id, user2_id FROM marriages 
            WHERE chat_id = ? AND (user1_id = ? OR user2_id = ?)
        ''', (chat_id, user_id, user_id)) as cursor:
            marriage = await cursor.fetchone()
            if marriage:
                partner_id = marriage['user2_id'] if marriage['user1_id'] == user_id else marriage['user1_id']
                return await get_user(partner_id, chat_id)
    return None


async def create_marriage(user1_id: int, user2_id: int, chat_id: int):
    """Создать брак"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO marriages (user1_id, user2_id, chat_id, married_at)
            VALUES (?, ?, ?, ?)
        ''', (user1_id, user2_id, chat_id, datetime.now().isoformat()))
        await db.commit()


async def delete_marriage(user_id: int, chat_id: int):
    """Удалить брак"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            DELETE FROM marriages WHERE chat_id = ? AND (user1_id = ? OR user2_id = ?)
        ''', (chat_id, user_id, user_id))
        await db.commit()


async def adopt_child(parent_id: int, child_id: int, chat_id: int):
    """Усыновить ребёнка"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO children (parent_id, child_id, chat_id, adopted_at)
            VALUES (?, ?, ?, ?)
        ''', (parent_id, child_id, chat_id, datetime.now().isoformat()))
        await db.commit()


async def disown_child(parent_id: int, child_id: int, chat_id: int):
    """Отказаться от ребёнка"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            DELETE FROM children WHERE parent_id = ? AND child_id = ? AND chat_id = ?
        ''', (parent_id, child_id, chat_id))
        await db.commit()


async def get_children(parent_id: int, chat_id: int):
    """Получить детей пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT u.* FROM children c
            JOIN users u ON c.child_id = u.user_id AND c.chat_id = u.chat_id
            WHERE c.parent_id = ? AND c.chat_id = ?
        ''', (parent_id, chat_id)) as cursor:
            return await cursor.fetchall()


async def get_parents(child_id: int, chat_id: int):
    """Получить родителей пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT u.* FROM children c
            JOIN users u ON c.parent_id = u.user_id AND c.chat_id = u.chat_id
            WHERE c.child_id = ? AND c.chat_id = ?
        ''', (child_id, chat_id)) as cursor:
            return await cursor.fetchall()


async def has_parent(child_id: int, chat_id: int):
    """Проверить, есть ли у пользователя родитель"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('''
            SELECT COUNT(*) FROM children WHERE child_id = ? AND chat_id = ?
        ''', (child_id, chat_id)) as cursor:
            result = await cursor.fetchone()
            return result[0] > 0
