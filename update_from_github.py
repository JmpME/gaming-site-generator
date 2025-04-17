import os
import requests
import zipfile
import io
import shutil
from datetime import datetime

GITHUB_REPO = "JumperME/gaming-site-bot"  # Замените на ваш репозиторий
GITHUB_BRANCH = "main"
REQUIRED_FILES = [
    'templates/index.php',
    'templates/redirect.php',
    'templates/config.php',
    'templates/jmpDG.php',
    'templates/styles.css',
    'templates/privacy.php',
    'templates/terms.php',
    'templates/check.php',
    'bot.py',
    'requirements.txt'
]

def download_repo():
    """Скачивает репозиторий с GitHub"""
    url = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/{GITHUB_BRANCH}.zip"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download repository: {response.status_code}")

def update_files():
    """Обновляет файлы из GitHub"""
    print("🔄 Starting update from GitHub...")
    
    # Создаем бэкап текущих файлов
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    os.makedirs(os.path.join(backup_dir, 'templates'), exist_ok=True)
    
    for file in REQUIRED_FILES:
        if os.path.exists(file):
            backup_path = os.path.join(backup_dir, file)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(file, backup_path)
    
    # Скачиваем и распаковываем репозиторий
    try:
        zip_content = download_repo()
        zip_file = io.BytesIO(zip_content)
        
        with zipfile.ZipFile(zip_file) as zf:
            repo_name = zf.namelist()[0].split('/')[0]
            
            # Обновляем файлы
            for file in REQUIRED_FILES:
                zip_path = f"{repo_name}/{file}"
                if zip_path in zf.namelist():
                    # Создаем директории если нужно
                    os.makedirs(os.path.dirname(file), exist_ok=True)
                    # Извлекаем файл
                    with zf.open(zip_path) as source, open(file, 'wb') as target:
                        shutil.copyfileobj(source, target)
                else:
                    print(f"⚠️ Warning: {file} not found in repository")
        
        print("✅ Update completed successfully!")
        print(f"📦 Backup created in: {backup_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Error during update: {str(e)}")
        # Восстанавливаем файлы из бэкапа
        for file in REQUIRED_FILES:
            backup_path = os.path.join(backup_dir, file)
            if os.path.exists(backup_path):
                os.makedirs(os.path.dirname(file), exist_ok=True)
                shutil.copy2(backup_path, file)
        print("🔄 Files restored from backup")
        return False

if __name__ == '__main__':
    update_files() 