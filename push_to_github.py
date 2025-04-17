import os
import subprocess
import datetime

def run_command(command):
    """Выполняет команду и возвращает результат"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode

def push_to_github():
    """Загружает все изменения на GitHub"""
    print("🔄 Загрузка на GitHub...")
    
    # Добавляем все файлы
    _, stderr, code = run_command("git add .")
    if code != 0:
        print(f"❌ Ошибка при git add: {stderr}")
        return False
    
    # Создаем коммит с текущей датой
    commit_message = f"Update bot files - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    _, stderr, code = run_command(f'git commit -m "{commit_message}"')
    if code != 0:
        print(f"❌ Ошибка при git commit: {stderr}")
        return False
    
    # Пушим изменения
    _, stderr, code = run_command("git push origin main")
    if code != 0:
        print(f"❌ Ошибка при git push: {stderr}")
        return False
    
    print("✅ Загрузка на GitHub завершена!")
    return True

if __name__ == "__main__":
    # Переходим в директорию бота
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    push_to_github() 