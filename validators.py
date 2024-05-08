import logging
import math
from config import config
from database import count_users, count_limits
from gpt import count_gpt_tokens

logging.basicConfig(
    level=config['LOGGING']['level'],
    format=config['LOGGING']['format'],
    filename=config['LOGGING']['filename'],
    filemode=config['LOGGING']['filemod']
)


def check_users_in_db(user_id):
    count = count_users(user_id)
    if count is None:
        return None, "Ошибка при работе с БД"
    if count > int(config['LIMITS']['MAX_USERS']):
        return None, "Превышено максимальное количество пользователей"
    return True, ""


def is_gpt_token_limit(messages, total_spent_tokens):
    all_tokens = count_gpt_tokens(messages) + total_spent_tokens
    if all_tokens > int(config['LIMITS']['MAX_USER_GPT_TOKENS']):
        return None, f"Превышен общий лимит GPT-токенов {int(config['LIMITS']['MAX_USER_GPT_TOKENS'])}"
    return all_tokens, ""


def is_tts_symbol_limit(user_id, message):
    text_symbols = len(message)
    all_symbols = count_limits(user_id, 'tts_symbols') + text_symbols

    if all_symbols >= int(config['LIMITS']['MAX_TTS_SYMBOLS']):
        msg = (f"Превышен общий лимит SpeechKit TTS {config['LIMITS']['MAX_TTS_SYMBOLS']}. Использовано: "
               f"{all_symbols} символов. Доступно: {int(config['LIMITS']['MAX_TTS_SYMBOLS']) - all_symbols}")
        return False, msg

    if text_symbols >= int(config['LIMITS']['MAX_USER_TTS_SYMBOLS']):
        msg = f"Превышен лимит SpeechKit TTS на запрос {config['LIMITS']['MAX_USER_TTS_SYMBOLS']}, в сообщении {text_symbols} символов"
        return False, msg

    return len(message), None


def is_stt_block_limit(user_id, duration):
    audio_blocks = math.ceil(duration / 15)
    all_blocks = count_limits(user_id, 'stt_blocks') + audio_blocks

    if duration >= 30:
        msg = "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"
        return None, msg

    if all_blocks >= int(config['LIMITS']['MAX_USER_STT_BLOCKS']):
        msg = f"Превышен общий лимит SpeechKit STT {int(config['LIMITS']['MAX_USER_STT_BLOCKS'])}. Использовано {all_blocks} блоков. Доступно: {int(config['LIMITS']['MAX_USER_STT_BLOCKS']) - all_blocks}"
        return None, msg

    return audio_blocks, None