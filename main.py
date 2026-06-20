import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import marriage, family, roles, profile

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    # Инициализация базы данных
    await init_db()
    logger.info("База данных инициализирована")
    
    # Создание бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрация роутеров
    dp.include_router(profile.router)
    dp.include_router(marriage.router)
    dp.include_router(family.router)
    dp.include_router(roles.router)
    
    logger.info("Бот запущен и работает...")
    
    # Запуск long polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
