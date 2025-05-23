import requests
import os
import shutil

def download_file(url, filename):
    """Скачивает отдельный файл с GitHub"""
    print(f"🔄 Downloading {filename}...")
    proxies = {
        'http': os.environ.get('http_proxy'),
        'https': os.environ.get('https_proxy')
    }
    
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded {filename}")
            return True
        else:
            print(f"❌ Failed to download {filename}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error downloading {filename}: {str(e)}")
        return False

def download_files():
    """Скачивает необходимые файлы с GitHub"""
    base_url = "https://raw.githubusercontent.com/JmpME/gaming-site-generator/main/"
    
    # Список файлов для скачивания
    REQUIRED_FILES = [
        "update_from_github.py",
        "bot.py",
        "requirements.txt",
        "config.json",
        "templates/index.php",
        "templates/style.css",
        "templates/script.js"
    ]
    
    # Скачиваем каждый файл
    for file in REQUIRED_FILES:
        url = base_url + file
        if not download_file(url, file):
            return False
    
    return True

if __name__ == '__main__':
    if download_files():
        print("\n✨ All files downloaded successfully!")
        print("\nNext steps:")
        print("1. pip3 install -r requirements.txt")
        print("2. python3 bot.py")
    else:
        print("\n❌ Failed to download some files. Please check the errors above.") 