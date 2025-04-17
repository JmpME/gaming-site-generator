#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime, timedelta

def check_bot():
    """Проверяет состояние бота и перезапускает его при необходимости"""
    
    # Проверяем лог файл
    if os.path.exists('restart.log'):
        with open('restart.log', 'r') as f:
            last_line = f.readlines()[-1]
            last_restart = datetime.strptime(last_line.split(': ')[0], '%Y-%m-%d %H:%M:%S.%f')
            
            # Если последний перезапуск был более 15 минут назад
            if datetime.now() - last_restart > timedelta(minutes=15):
                print("Bot seems to be stuck, restarting...")
                # Создаем триггер для перезапуска
                with open('restart_trigger', 'w') as f:
                    f.write(f'check_restart_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
                return True
    else:
        print("No restart log found, starting bot...")
        return True
    
    return False

if __name__ == '__main__':
    needs_restart = check_bot()
    if needs_restart:
        # Запускаем бота
        os.system('python3 bot.py &')
        print("Bot started") 