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


def add_message(user_id, full_message):
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        message, role, total_gpt_tokens, tts_symbols, stt_blocks = full_message
        cursor.execute('''
            INSERT INTO messages (user_id, message, role, total_gpt_tokens, tts_symbols, stt_blocks)
            VALUES (?, ?, ?, ?, ?, ?)''',
                       (user_id, message, role, total_gpt_tokens, tts_symbols, stt_blocks))
        con.commit()
        logging.info(f"DATABASE: INSERT INTO messages"
                     f"VALUES ({user_id}, {message}, {role}, {total_gpt_tokens}, {tts_symbols}, {stt_blocks})")
    except sqlite3.Error as e:
        logging.error(e)
    finally:
        con.close()


def count_users(user_id):
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        cursor.execute('''SELECT COUNT(DISTINCT user_id) FROM messages WHERE user_id <> ?''', (user_id,))
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        logging.error(e)
    finally:
        con.close()


def select_n_last_messages(user_id, n_last_messages=4):
    messages = []
    total_spent_tokens = 0
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        cursor.execute('''
        SELECT message, role, total_gpt_tokens FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ?''',
                       (user_id, n_last_messages))
        data = cursor.fetchall()

        if data and data[0]:
            for message in reversed(data):
                messages.append({'text': message[0], 'role': message[1]})
                total_spent_tokens = max(total_spent_tokens, message[2])
            return messages, total_spent_tokens
    except sqlite3.Error as e:
        logging.error(e)
        return messages, total_spent_tokens
    finally:
        con.close()


def count_limits(user_id, limit_type):
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        cursor.execute(f'''SELECT SUM({limit_type}) FROM messages WHERE user_id=?''', (user_id,))
        data = cursor.fetchone()
        if data and data[0]:
            logging.info(f"DATABASE: user_id={user_id} used {data[0]} {limit_type}")
            return data[0]
        else:
            return 0
    except sqlite3.Error as e:
        logging.error(e)
        return 0
    finally:
        con.close()