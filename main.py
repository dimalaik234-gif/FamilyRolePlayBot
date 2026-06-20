import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, BOT_NAME, BOT_VERSION
from database import init_db
from handlers import marriage, family, roles, profile

# ═══════════════════════════════════════════════
#              FAMILY RP BOT v1.0.0
# ═══════════════════════════════════════════════

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_banner():
    """Красивый баннер при запуске"""
    banner = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║         👨‍👩‍👧‍👦 FAMILY RP BOT 👨‍👩‍👧‍👦           ║
║              Version {BOT_VERSION}                ║
║                                           ║
║   💍 Браки  👶 Усыновления  🎭 Роли      ║
║                                           ║
╚═══════════════════════════════════════════╝
    """
    print(banner)


async def main():
    """Главная функция запуска бота"""
    print_banner()
    
    # Инициализация базы данных
    logger.info("🗄️  Инициализация базы данных...")
    await init_db()
    logger.info("✅ База данных готова")
    
    # Создание бота и диспетчера
    logger.info("🤖 Создание экземпляра бота...")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрация роутеров
    logger.info("📡 Регистрация обработчиков...")
    dp.include_router(profile.router)
    dp.include_router(marriage.router)
    dp.include_router(family.router)
    dp.include_router(roles.router)
    logger.info("✅ Все обработчики зарегистрированы")
    
    logger.info("🚀 Запуск long polling...")
    logger.info("✨ Бот работает! Нажмите Ctrl+C для остановки")
    
    # Запуск long polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("👋 Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Получен сигнал остановки")
