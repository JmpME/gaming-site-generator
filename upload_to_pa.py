import os
import requests
import time

# Ваши данные
API_TOKEN = "1ba8059677293b6cd21bbc975dee3083d4444a00"
USERNAME = "JumperME"
BASE_URL = "https://www.pythonanywhere.com/api/v0/user/{username}/files/path{path}"

# Точный путь к директории бота на компьютере
LOCAL_BOT_DIR = "/Users/vladimir/Work/Cursor_site/bot"

def upload_file(local_path, remote_path):
    """Загружает файл на PythonAnywhere"""
    try:
        with open(local_path, 'rb') as f:
            content = f.read()
        
        url = BASE_URL.format(username=USERNAME, path=remote_path)
        headers = {'Authorization': f'Token {API_TOKEN}'}
        
        response = requests.post(url, headers=headers, files={'content': content})
        
        if response.status_code == 200:
            print(f"✅ {os.path.basename(local_path)}")
            return True
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 5))
            print(f"⏳ Ждем {retry_after}с...")
            time.sleep(retry_after)
            return upload_file(local_path, remote_path)
        else:
            print(f"❌ {os.path.basename(local_path)}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {os.path.basename(local_path)}: {str(e)}")
        return False

def create_directory(remote_path):
    """Создает директорию на PythonAnywhere"""
    try:
        url = BASE_URL.format(username=USERNAME, path=remote_path)
        headers = {'Authorization': f'Token {API_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
            
        response = requests.post(url, headers=headers, files={'content': b''})
        return response.status_code in [200, 400]
    except:
        return False

def upload_directory(local_dir, remote_dir):
    """Загружает директорию на PythonAnywhere"""
    create_directory(remote_dir)
    
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, local_dir)
            remote_path = os.path.join(remote_dir, rel_path)
            
            remote_dir_path = os.path.dirname(remote_path)
            create_directory(remote_dir_path)
                
            upload_file(local_path, remote_path)

# Загружаем основные файлы
files_to_upload = [
    (os.path.join(LOCAL_BOT_DIR, 'bot.py'), '/bot/bot.py'),
    (os.path.join(LOCAL_BOT_DIR, 'requirements.txt'), '/bot/requirements.txt'),
    (os.path.join(LOCAL_BOT_DIR, 'config.json'), '/bot/config.json'),
    (os.path.join(LOCAL_BOT_DIR, 'generators.py'), '/bot/generators.py'),
    (os.path.join(LOCAL_BOT_DIR, 'styles.css'), '/bot/styles.css'),
    (os.path.join(LOCAL_BOT_DIR, 'start_bot.sh'), '/bot/start_bot.sh'),
]

print("🔄 Загрузка файлов...")

# Загружаем шаблоны
upload_directory(os.path.join(LOCAL_BOT_DIR, 'templates'), '/bot/templates')

# Загружаем основные файлы
for local, remote in files_to_upload:
    upload_file(local, remote)

print("✅ Загрузка завершена!") 