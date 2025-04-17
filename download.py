import os
import requests

REPO = "JmpME/gaming-site-generator"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

# Список файлов для скачивания
FILES = [
    'bot.py',
    'requirements.txt',
    'update_from_github.py',
    'templates/index.html',
    'templates/style.css',
    'templates/script.js'
]

def download():
    # Создаем директорию templates если нужно
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    for file in FILES:
        url = f"{BASE_URL}/{file}"
        print(f"Скачиваю {file}...")
        
        try:
            r = requests.get(url)
            r.raise_for_status()
            
            with open(file, 'wb') as f:
                f.write(r.content)
            print(f"✅ {file} готово")
            
        except Exception as e:
            print(f"❌ Ошибка при скачивании {file}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    if download():
        print("\n✨ Все файлы скачаны!")
        print("\nТеперь выполните:")
        print("pip3 install -r requirements.txt")
        print("python3 bot.py") 