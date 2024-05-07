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
    bot.send_message(message.chat.id, 'Кушман')
    create_database()
    add_message(26, ['avs', 'asdf', 0, 0, 0])


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    checked_user = check_users_in_db(user_id)
    if checked_user:
        bot.send_message(message.chat.id, bot_templates['say_generate_tts'])
        bot.register_next_step_handler(message, text_to_speech)
    else:
        bot.send_message(message.chat.id, bot_templates['hard_user_limit'])


def text_to_speech(message):
    user_id = message.from_user.id

    if message.text.isdigit():
        bot.send_message(message.chat.id, 'Введите текст, а не число!')

    elif message.text == '/stop':#!!!!!!!!!!!!!!!!!!!!!!!!!
        return

    else:
        symbols, msg = is_tts_symbol_limit(message)

        if not symbols:
            bot.send_message(message.chat.id, msg)

        else:
            # insert_data(user_id, message.text, symbols)
            add_message(user_id, [message.text, 'test_tts', 0, symbols, 0])
            success, response = tts(message.text)

            if success:
                with open("output.ogg", "wb") as audio_file:
                    audio_file.write(response)
                bot.send_audio(message.chat.id, audio=open('output.ogg', 'rb'))
                logging.info("Аудиофайл успешно сохранен как output.ogg")
            else:
                logging.error("Ошибка:", response)

    bot.register_next_step_handler(message, text_to_speech)


@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    checked_user = check_users_in_db(user_id)
    if checked_user:
        bot.send_message(message.chat.id, bot_templates['say_generate_stt'])
        bot.register_next_step_handler(message, speech_to_text)
    else:
        bot.send_message(message.chat.id, bot_templates['hard_user_limit'])


def speech_to_text(message):
    user_id = message.from_user.id

    if not message.voice:
        bot.send_message(message.chat.id, bot_templates['if_not_voice'])

    else:
        blocks, msg = is_stt_block_limit(message, message.voice.duration)

        if not blocks:
            bot.send_message(message.chat.id, msg)

        else:
            file_id = message.voice.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            status, text = stt(file)

            if status:
                add_message(user_id, [message.text, 'test_tts', 0, 0, blocks])
                # insert_data(user_id, text, blocks)
                bot.send_message(message.chat.id, text, reply_to_message_id=message.id)
                logging.info("Аудиофайл успешно переработан в текст.")
            else:
                logging.error("Ошибка:", text)

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
        print(last_messages)

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
        print(e)
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")


bot.polling()