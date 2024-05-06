import logging
import sqlite3

from config import config

logging.basicConfig(
    level=config['LOGGING']['level'],
    format=config['LOGGING']['format'],
    filename=config['LOGGING']['filename'],
    filemode=config['LOGGING']['filemod']
)
database = config['MAIN']['DB_FILE']


def create_database():
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            message TEXT, 
            role TEXT,
            total_gpt_tokens INTEGER,
            tts_symbols INTEGER,
            stt_blocks INTEGER)
        ''')
        logging.info("DATABASE: table was created")
    except sqlite3.Error as e:
        logging.error(e)
    finally:
        con.close()