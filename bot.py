import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import threading
import time
import subprocess
import sys
import pytz
from datetime import datetime
import zipfile
import io
import random
import string
<<<<<<< HEAD
import tempfile
import shutil

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы
TIMEZONE = pytz.timezone('Europe/Moscow')
RESTART_INTERVAL = 6 * 60 * 60  # 6 часов в секундах
VERSION = "2.2.0"

# Список стилей
STYLES = ["classic", "dark", "neon", "gradient", "minimal"]

# Загрузка конфигурации
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Файл config.json не найден")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("Ошибка в формате config.json")
        sys.exit(1)

config = load_config()
TOKEN = config.get('token')
if not TOKEN:
    logger.error("Токен не найден в config.json")
    sys.exit(1)

ALLOWED_USERS = config.get('allowed_users', [])

def randomize_content(content):
    """Рандомизирует контент сайта"""
    # Выбираем случайный стиль
    style = random.choice(STYLES)
    content = content.replace('<body>', f'<body class="{style}">')
    
    return content

def generate_site(theme=None):
    """Генерирует сайт с заданной темой"""
    try:
        # Создаем временную директорию
        with tempfile.TemporaryDirectory() as temp_dir:
            # Копируем шаблоны
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
            for file in os.listdir(templates_dir):
                if file.endswith(('.php', '.css', '.html')):
                    shutil.copy2(
                        os.path.join(templates_dir, file),
                        os.path.join(temp_dir, file)
                    )
            
            # Рандомизируем контент
            index_path = os.path.join(temp_dir, 'index.php')
            with open(index_path, 'r') as f:
                content = f.read()
            
            content = randomize_content(content)
            
            with open(index_path, 'w') as f:
                f.write(content)
            
            # Создаем ZIP-архив
            zip_path = os.path.join(temp_dir, 'site.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file != 'site.zip':
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
            
            return zip_path
    except Exception as e:
        logger.error(f"Ошибка при генерации сайта: {e}")
        return None
=======
import json
import subprocess
import signal
import time
import threading
from datetime import datetime

VERSION = "2.2.0"

# Варианты для рандомизации
SITE_TITLES = [
    "Premium Gaming Universe 2025",
    "Elite Gaming World 2025",
    "Ultimate Gaming Zone 2025",
    "Pro Gaming Hub 2025",
    "Gaming Paradise 2025",
    "Gaming Masters 2025",
    "Gaming Legends 2025",
    "Gaming Empire 2025"
]

GAME_NAMES = [
    "NexusPlay",
    "GameVortex",
    "PlayMaster",
    "GamePulse",
    "PlayNova",
    "GameForge",
    "PlayPrime",
    "GameNexus",
    "PlayElite",
    "GameSphere"
]

BADGES = [
    ["Elite Choice", "Premium Pick", "Top Rated", "Best Choice", "Editor's Choice"],
    ["3M+ Users", "5M+ Players", "2M+ Gamers", "4M+ Active", "1M+ Daily"]
]

def randomize_content(template):
    """Заменяет статический контент на случайный"""
    # Случайные значения
    title = random.choice(SITE_TITLES)
    game_name = random.choice(GAME_NAMES)
    badge1 = random.choice(BADGES[0])
    badge2 = random.choice(BADGES[1])
    rating = f"{random.uniform(4.5, 5.0):.1f}"
    users = f"{random.randint(1, 5)}M+"
    langs = str(random.randint(20, 50))
    
    # Замены в шаблоне
    template = template.replace("Premium Gaming Universe 2025", title)
    template = template.replace("NexusPlay", game_name)
    template = template.replace("Elite Choice", badge1)
    template = template.replace("3M+ Users", badge2)
    template = template.replace("⭐ 4.9", f"⭐ {rating}")
    template = template.replace("👥 3M+ active", f"👥 {users} active")
    template = template.replace("🌍 30 langs", f"🌍 {langs} langs")
    
    return template

# Загружаем конфигурацию из JSON
with open('config.json', 'r') as f:
    config = json.load(f)

# Получаем токен бота и список разрешенных пользователей
TOKEN = config.get('token')
ALLOWED_USERS = config.get('allowed_users', [])

def generate_site(theme=None):
    """Генерация сайта с готовыми файлами из templates"""
    files = {}
    template_files = [
        'index.php',
        'redirect.php',
        'config.php',
        'jmpDG.php',
        'styles.css',
        'privacy.php',
        'terms.php',
        'check.php'
    ]
    
    for file in template_files:
        with open(f'templates/{file}', 'r') as f:
            content = f.read()
            # Применяем рандомизацию только к index.php
            if file == 'index.php':
                content = randomize_content(content)
            files[file] = content
    
    return files
>>>>>>> bbe2c17869f75ab1b0ed0e2a1e7eaf15cb6e208b

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ALLOWED_USERS:
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    
<<<<<<< HEAD
    await update.message.reply_text(
        "Привет! Я бот для генерации сайтов.\n"
        "Доступные команды:\n"
        "/generate - Сгенерировать сайт\n"
        "/theme [цвет] - Установить тему сайта\n"
        "/update - Обновить бота"
=======
    update.message.reply_text(
        f"🎮 Gaming Site Generator v{VERSION}\n\n"
        "Available commands:\n"
        "/generate - create site with random theme\n"
        "/theme [color] - create site with specific color theme\n"
        "/update - update bot to latest version\n"
        "/restart - restart bot service\n\n"
        "Available colors: purple, blue, cyber, neon, sunset, forest, cherry, midnight, aurora, volcano, galaxy, ocean\n\n"
        "🎯 All sites include:\n"
        "- Responsive design\n"
        "- Palladium integration\n"
        "- Tracking parameters\n"
        "- Mobile optimization"
>>>>>>> bbe2c17869f75ab1b0ed0e2a1e7eaf15cb6e208b
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ALLOWED_USERS:
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    
    try:
        zip_path = generate_site()
        if zip_path:
            with open(zip_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename='site.zip',
                    caption='Ваш сайт готов!'
                )
            os.remove(zip_path)
        else:
            await update.message.reply_text("Произошла ошибка при генерации сайта.")
    except Exception as e:
        logger.error(f"Ошибка при генерации сайта: {e}")
        await update.message.reply_text("Произошла ошибка при генерации сайта.")

async def theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ALLOWED_USERS:
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    
    if not context.args:
        await update.message.reply_text("Укажите цвет темы. Например: /theme blue")
        return
    
    color = context.args[0].lower()
    try:
        zip_path = generate_site(color)
        if zip_path:
            with open(zip_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename='site.zip',
                    caption=f'Сайт с темой {color} готов!'
                )
            os.remove(zip_path)
        else:
            await update.message.reply_text("Произошла ошибка при генерации сайта.")
    except Exception as e:
        logger.error(f"Ошибка при установке темы: {e}")
        await update.message.reply_text("Произошла ошибка при установке темы.")

async def update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ALLOWED_USERS:
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    
    try:
        from update_from_github import update_from_github
        success = update_from_github()
        if success:
            await update.message.reply_text("Бот успешно обновлен! Перезапуск...")
            subprocess.Popen(['python3', 'restart.py'])
        else:
            await update.message.reply_text("Ошибка при обновлении бота.")
    except Exception as e:
        logger.error(f"Ошибка при обновлении бота: {e}")
        await update.message.reply_text("Произошла ошибка при обновлении бота.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")

def auto_restart():
    while True:
        time.sleep(RESTART_INTERVAL)
        logger.info("Автоматический перезапуск бота...")
        subprocess.Popen(['python3', 'restart.py'])

def update_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        update.message.reply_text("⛔ Access denied")
        return
    
    update.message.reply_text("🔄 Starting update from GitHub...")
    try:
        # Импортируем функцию обновления
        from update_from_github import update_files
        
        # Запускаем обновление
        success = update_files()
        
        if success:
            update.message.reply_text(f"✅ Update completed successfully!\n✨ Current version: v{VERSION}\n🔄 Restarting bot...")
            
            # Создаем файл-триггер для перезапуска
            with open('restart_trigger', 'w') as f:
                f.write(f'update_restart_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            # Завершаем текущий процесс
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            update.message.reply_text("❌ Update failed, check server logs for details")
            
    except Exception as e:
        update.message.reply_text(f"❌ Error during update: {str(e)}")

def restart_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        update.message.reply_text("⛔ Access denied")
        return
    
    update.message.reply_text("🔄 Restarting bot...")
    try:
        # Создаем файл-триггер для перезапуска
        with open('restart_trigger', 'w') as f:
            f.write(f'manual_restart_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Завершаем текущий процесс
        os.kill(os.getpid(), signal.SIGTERM)
        
    except Exception as e:
        update.message.reply_text(f"❌ Error during restart: {str(e)}")

def auto_restart():
    """Автоматический перезапуск каждые 10 минут"""
    while True:
        time.sleep(600)  # 10 минут
        try:
            # Создаем файл-триггер для перезапуска
            with open('restart_trigger', 'w') as f:
                f.write(f'auto_restart_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            print(f"Auto-restart triggered at {datetime.now()}")
            # Завершаем текущий процесс
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception as e:
            print(f"Error in auto_restart: {str(e)}")

def log_restart(update, context):
    if os.path.exists('restart.log'):
        with open('restart.log', 'a') as f:
            f.write(f"{datetime.now()}: Bot restarted\n")
    else:
        with open('restart.log', 'w') as f:
            f.write(f"{datetime.now()}: Bot started\n")

def main():
<<<<<<< HEAD
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("theme", theme))
    application.add_handler(CommandHandler("update", update_bot))
    application.add_error_handler(error_handler)
    
    # Запуск потока автоматического перезапуска
    restart_thread = threading.Thread(target=auto_restart)
    restart_thread.daemon = True
    restart_thread.start()
    
    # Запуск бота
    logger.info(f"Bot started v{VERSION}")
    application.run_polling()
=======
    # Проверяем наличие файла-триггера для перезапуска
    if os.path.exists('restart_trigger'):
        os.remove('restart_trigger')
        time.sleep(1)  # Даем время на завершение старого процесса

    # Запускаем поток для автоматического перезапуска
    restart_thread = threading.Thread(target=auto_restart, daemon=True)
    restart_thread.start()
    
    # Инициализируем бота
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate_site_command))
    dp.add_handler(CommandHandler("theme", theme_command))
    dp.add_handler(CommandHandler("update", update_command))
    dp.add_handler(CommandHandler("restart", restart_command))
    
    # Добавляем обработчик для логирования перезапусков
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, log_restart))

    print(f"Bot started v{VERSION}")
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()
>>>>>>> bbe2c17869f75ab1b0ed0e2a1e7eaf15cb6e208b

if __name__ == '__main__':
    main() 