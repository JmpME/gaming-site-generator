import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import zipfile
import io
import random
import string
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

def create_zip(files):
    """Создание ZIP архива в памяти"""
    memory_zip = io.BytesIO()
    with zipfile.ZipFile(memory_zip, 'w') as zf:
        for fname, content in files.items():
            zf.writestr(fname, content)
    memory_zip.seek(0)
    return memory_zip

def start(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        update.message.reply_text("⛔ Access denied")
        return
    
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
    )

def generate_site_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        update.message.reply_text("⛔ Access denied")
        return

    update.message.reply_text("🔄 Generating site...")
    
    try:
        files = generate_site()
        zip_file = create_zip(files)
        
        update.message.reply_document(
            document=zip_file,
            filename=f'gaming_site_{random_string()}.zip',
            caption="✅ Site generated successfully!"
        )
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

def theme_command(update, context):
    if update.message.from_user.username not in ALLOWED_USERS:
        update.message.reply_text("⛔ Access denied")
        return

    theme = ' '.join(context.args) if context.args else None
    
    if not theme:
        update.message.reply_text("Please specify a theme color!")
        return
        
    update.message.reply_text(f"🔄 Generating site with {theme} theme...")
    
    try:
        files = generate_site(theme)
        zip_file = create_zip(files)
        
        update.message.reply_document(
            document=zip_file,
            filename=f'gaming_site_{theme}_{random_string()}.zip',
            caption="✅ Site generated successfully!"
        )
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

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

if __name__ == '__main__':
    main() 