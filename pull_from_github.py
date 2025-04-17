import os
import subprocess

def run_command(command):
    """Выполняет команду и возвращает результат"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode

def pull_from_github():
    """Скачивает все изменения с GitHub"""
    print("🔄 Скачивание с GitHub...")
    
    # Если директории нет - клонируем репозиторий
    if not os.path.exists('.git'):
        _, stderr, code = run_command("git clone https://github.com/JmpME/gaming-site-generator.git .")
        if code != 0:
            print(f"❌ Ошибка при git clone: {stderr}")
            return False
    
    # Если директория есть - делаем pull
    else:
        # Сначала сбрасываем все локальные изменения
        _, stderr, code = run_command("git reset --hard HEAD")
        if code != 0:
            print(f"❌ Ошибка при git reset: {stderr}")
            return False
            
        _, stderr, code = run_command("git pull origin main")
        if code != 0:
            print(f"❌ Ошибка при git pull: {stderr}")
            return False
    
    print("✅ Скачивание с GitHub завершено!")
    return True

if __name__ == "__main__":
    # Переходим в директорию бота
    os.chdir('/home/JumperME/bot')
    pull_from_github() 