import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import zipfile
import io
import random
import string
import json
from generators import (
    generate_index,
    generate_redirect,
    generate_config,
    get_palladium_template,
    get_color_scheme,
    generate_unique_names
)

# Загружаем конфигурацию из JSON
with open('bot/config.json', 'r') as f:
    config = json.load(f)

ALLOWED_USERS = config['allowed_users']
BOT_TOKEN = config['bot_token']

def generate_site(theme=None):
    """Генерация сайта с уникальными параметрами"""
    files = {
        'index.php': generate_index(theme),
        'redirect.php': generate_redirect(),
        'config.php': generate_config(),
        'jmpDG.php': get_palladium_template()
    }
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
        "🎮 Welcome to Gaming Site Generator!\n\n"
        "Available commands:\n"
        "/generate - create site with random theme\n"
        "/theme [color] - create site with specific color theme\n"
        "Available colors: purple, blue, green, red, dark\n\n"
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

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate_site_command))
    dp.add_handler(CommandHandler("theme", theme_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 