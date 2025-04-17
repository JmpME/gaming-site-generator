import os
import requests
import time

# IP адрес вашего компьютера в локальной сети
LOCAL_IP = "http://YOUR_LOCAL_IP:8000"  # Замените на ваш IP
BOT_FILES = [
    'bot.py',
    'requirements.txt',
    'config.json',
    'generators.py',
    'styles.css',
    'start_bot.sh'
]

def download_file(filename, save_path):
    """Скачивает файл с локального компьютера"""
    try:
        url = f"{LOCAL_IP}/{filename}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ {filename}")
            return True
        else:
            print(f"❌ {filename}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {filename}: {str(e)}")
        return False

def download_directory(dir_name):
    """Скачивает директорию с локального компьютера"""
    try:
        url = f"{LOCAL_IP}/{dir_name}/"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            # Предполагаем, что получаем список файлов в формате HTML
            # Здесь нужно будет извлечь имена файлов из HTML
            files = [f for f in response.text.split('"') if f.endswith('.html')]
            
            for file in files:
                download_file(f"{dir_name}/{file}", f"/home/JumperME/bot/{dir_name}/{file}")
            return True
    except Exception as e:
        print(f"❌ {dir_name}: {str(e)}")
        return False

print("🔄 Скачивание файлов...")

# Скачиваем основные файлы
for file in BOT_FILES:
    download_file(file, f"/home/JumperME/bot/{file}")

# Скачиваем templates
download_directory('templates')

print("✅ Скачивание завершено!") 