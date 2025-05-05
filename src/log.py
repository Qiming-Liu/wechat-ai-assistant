from src.config import LOG_DIR
import os
import datetime
import time

def init_log():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def log(chat_id, message):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f"{today}_{chat_id}.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        current_time = time.time()
        timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {chat_id}: {message}\n")
        

def log_ai(chat_id, message):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f"{today}_{chat_id}.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        current_time = time.time()
        timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {chat_id}: {message}\n")
