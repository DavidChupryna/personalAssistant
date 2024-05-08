import logging
import telebot
from config import config
from database import create_database, add_message, select_n_last_messages
from speechKit import tts, stt
from validators import check_users_in_db, is_tts_symbol_limit, is_stt_block_limit, is_gpt_token_limit
from info import bot_templates
from gpt import ask_gpt

bot = telebot.TeleBot(token=config['CREDENTIALS']['BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, '')
    create_database()


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, 'хелп Кушик')#!!!!!!!!!!!!!!!!!!!!!


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    checked_user, error_message = check_users_in_db(user_id)
    if checked_user:
        bot.send_message(message.chat.id, bot_templates['say_generate_tts'])
        bot.register_next_step_handler(message, text_to_speech)
    else:
        bot.send_message(message.chat.id, error_message)


def text_to_speech(message):
    user_id = message.from_user.id

    if message.text.isdigit():
        bot.send_message(message.chat.id, 'Введите текст, а не число!')

    elif message.text == '/stop' or message.text == '/exit':#!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(message.chat.id, 'Функция остановлена')
        return

    else:
        symbols, msg = is_tts_symbol_limit(user_id, message.text)

        if not symbols:
            bot.send_message(message.chat.id, msg)

        else:
            add_message(user_id, [message.text, 'test_tts', 0, symbols, 0])
            success, response = tts(message.text)

            if success:
                with open("output.ogg", "wb") as audio_file:
                    audio_file.write(response)
                bot.send_message(message.chat.id, 'Ваш текст обрабатывается, ожидайте...')
                bot.send_audio(message.chat.id, audio=open('output.ogg', 'rb'))
                logging.info("The audio file was successfully saved as output.ogg")
            else:
                logging.error("Error:", response)

    bot.register_next_step_handler(message, text_to_speech)


@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    checked_user, error = check_users_in_db(user_id)
    if checked_user:
        bot.send_message(message.chat.id, bot_templates['say_generate_stt'])
        bot.register_next_step_handler(message, speech_to_text)
    else:
        bot.send_message(message.chat.id, error)


def speech_to_text(message):
    user_id = message.from_user.id

    if message.text == '/stop' or message.text == '/exit':#!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(message.chat.id, 'Функция остановлена')
        return

    elif not message.voice:
        bot.send_message(message.chat.id, bot_templates['if_not_voice'])

    else:
        blocks, msg = is_stt_block_limit(user_id, message.voice.duration)

        if not blocks:
            bot.send_message(message.chat.id, msg)

        else:
            file_id = message.voice.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            status, text = stt(file)

            if status:
                add_message(user_id, [message.text, 'test_tts', 0, 0, blocks])
                bot.send_message(message.chat.id, 'Ожидайте...')
                bot.send_message(message.chat.id, text, reply_to_message_id=message.id)
                bot.send_message(message.chat.id, 'Для выхода из функции speech to text, '
                                                  'воспользуйтесь командой /stop или /exit')#!!!!!!
                logging.info("The audio file has been successfully processed into text.")
            else:
                logging.error("Error:", text)

    bot.register_next_step_handler(message, speech_to_text)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        user_id = message.from_user.id

        status_check_users, error_message = check_users_in_db(user_id)

        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        full_user_message = [message.text, 'user', 0, 0, 0]
        add_message(user_id=user_id, full_message=full_user_message)
        last_messages, total_spent_tokens = select_n_last_messages(user_id, int(config['LIMITS']['COUNT_LAST_MESSAGE']))
        total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)

        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return

        total_gpt_tokens += tokens_in_answer

        full_gpt_message = [answer_gpt, 'assistant', total_gpt_tokens, 0, 0]
        add_message(user_id=user_id, full_message=full_gpt_message)

        bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)
    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    try:
        user_id = message.from_user.id

        status_check_users, error_message = check_users_in_db(user_id)
        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)
        if error_message:
            bot.send_message(user_id, error_message)
            return

        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        status_stt, stt_text = stt(file)

        if not status_stt:
            bot.send_message(user_id, stt_text)
            return

        add_message(user_id=user_id, full_message=[stt_text, 'user', 0, 0, stt_blocks])

        last_messages, total_spent_tokens = select_n_last_messages(user_id, int(config['LIMITS']['COUNT_LAST_MESSAGE']))
        total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return

        total_gpt_tokens += tokens_in_answer
        tts_symbols, error_message = is_tts_symbol_limit(user_id, answer_gpt)

        add_message(user_id=user_id, full_message=[answer_gpt, 'assistant', total_gpt_tokens, tts_symbols, 0])

        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_tts, voice_response = tts(answer_gpt)
        if status_tts:
            bot.send_voice(user_id, voice_response, reply_to_message_id=message.id)
        else:
            bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)

    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, "Не получилось ответить. Попробуй записать другое сообщение")


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


bot.polling()