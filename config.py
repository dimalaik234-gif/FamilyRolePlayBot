import os

# ═══════════════════════════════════════════════
#           FAMILY RP BOT - CONFIGURATION
# ═══════════════════════════════════════════════

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8898239222:AAFyly_OY2zfqC-iTCZqhiC_SOC-WZgaK-A")

# Путь к базе данных
DB_PATH = "database.db"

# Информация о боте
BOT_NAME = "Family RP Bot"
BOT_VERSION = "1.0.0"
BOT_AUTHOR = "Your Name"

# Доступные роли
AVAILABLE_ROLES = {
    "Лупа": "🔴",
    "Пупа": "🟡",
    "Залупа": "🟣",
    "Залупомэн": "🦸"
}
