import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import zipfile
import io
import random
import string
import json
import subprocess
import signal
import time
import threading
from datetime import datetime, timedelta
import pytz
import asyncio

VERSION = "2.1.1"

# Загружаем конфигурацию из JSON
with open('config.json', 'r') as f:
    config = json.load(f)

# Получаем токен бота и список разрешенных пользователей
TOKEN = config['token']
ALLOWED_USERS = config['allowed_users']

# Устанавливаем часовой пояс
TIMEZONE = pytz.timezone('Europe/Kiev')

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
            files[file] = f.read()
    
    return files

def create_zip(files):
    """Создание ZIP архива в памяти"""
    memory_zip = io.BytesIO()
    with zipfile.ZipFile(memory_zip, 'w') as zf:
        for fname, content in files.items():
            zf.writestr(fname, content)
    memory_zip.seek(0)
    return memory_zip

async def start(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access denied")
        return
    
    await update.message.reply_text(
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
    )

async def generate_site_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access denied")
        return

    await update.message.reply_text("🔄 Generating site...")
    
    try:
        files = generate_site()
        zip_file = create_zip(files)
        
        await update.message.reply_document(
            document=zip_file,
            filename=f'gaming_site_{random_string()}.zip',
            caption="✅ Site generated successfully!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def theme_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access denied")
        return

    theme = ' '.join(context.args) if context.args else None
    
    if not theme:
        await update.message.reply_text("Please specify a theme color!")
        return
        
    await update.message.reply_text(f"🔄 Generating site with {theme} theme...")
    
    try:
        files = generate_site(theme)
        zip_file = create_zip(files)
        
        await update.message.reply_document(
            document=zip_file,
            filename=f'gaming_site_{theme}_{random_string()}.zip',
            caption="✅ Site generated successfully!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

async def update_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access denied")
        return
    
    await update.message.reply_text("🔄 Starting update from GitHub...")
    try:
        # Импортируем функцию обновления
        from update_from_github import update_files
        
        # Запускаем обновление
        success = update_files()
        
        if success:
            await update.message.reply_text(f"✅ Update completed successfully!\n✨ Current version: v{VERSION}\n🔄 Restarting bot...")
            
            # Создаем файл-триггер для перезапуска
            with open('restart_trigger', 'w') as f:
                f.write(f'update_restart_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            # Завершаем текущий процесс
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            await update.message.reply_text("❌ Update failed, check server logs for details")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error during update: {str(e)}")

async def restart_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access denied")
        return
    
    await update.message.reply_text("🔄 Restarting bot...")
    try:
        # Создаем файл-триггер для перезапуска
        with open('restart_trigger', 'w') as f:
            f.write(f'manual_restart_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Завершаем текущий процесс
        os.kill(os.getpid(), signal.SIGTERM)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error during restart: {str(e)}")

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

async def log_restart(update, context):
    if os.path.exists('restart.log'):
        with open('restart.log', 'a') as f:
            f.write(f"{datetime.now()}: Bot restarted\n")
    else:
        with open('restart.log', 'w') as f:
            f.write(f"{datetime.now()}: Bot started\n")

async def main():
    # Проверяем наличие файла-триггера для перезапуска
    if os.path.exists('restart_trigger'):
        os.remove('restart_trigger')
        time.sleep(1)  # Даем время на завершение старого процесса

    # Запускаем поток для автоматического перезапуска
    restart_thread = threading.Thread(target=auto_restart, daemon=True)
    restart_thread.start()
    
    # Инициализируем приложение без job_queue
    application = Application.builder().token(TOKEN).job_queue(None).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_site_command))
    application.add_handler(CommandHandler("theme", theme_command))
    application.add_handler(CommandHandler("update", update_command))
    application.add_handler(CommandHandler("restart", restart_command))
    
    # Добавляем обработчик для логирования перезапусков
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, log_restart))

    print(f"Bot started v{VERSION}")
    
    # Запускаем бота
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main()) 