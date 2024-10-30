import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def log_activity(activity):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open('activity_log.txt', 'a') as f:
        f.write(f'{timestamp} {activity}\n')