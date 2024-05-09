import configparser

config = configparser.ConfigParser()
config['LOGGING'] = {
    'level': 'INFO',
    'format': '%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s',
    'filename': 'log_file.txt',
    'filemod': 'w'
}

config['GPT'] = {
    'URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'TEMPERATURE': '0.6',
    'TOKENIZE_URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
}

config['SPEECH_KIT'] = {
    'TTS_URL': 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
    'STT_URL': 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
}

config['LIMITS'] = {
    'MAX_MESSAGE_TOKENS': '50',
    'MAX_USERS': '2',
    'MAX_USER_TTS_SYMBOLS': '2000',
    'MAX_TTS_SYMBOLS': '1000',
    'MAX_USER_STT_BLOCKS': '7',
    'MAX_USER_GPT_TOKENS': '2000',
    'MAX_ANSWER_GPT_TOKENS': '64',
    'COUNT_LAST_MESSAGE': '4'
}

config['PROMPTS'] = {
    'SYSTEM': 'Ты веселый собеседник. Общайся с пользователем на "ты" и используй юмор. '
              'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь. '
              'Изображай человека',
}

config['MAIN'] = {
    'DB_FILE': 'messages.db'
}

config['CREDENTIALS'] = {
    'FOLDER_ID': "b1gmco3nm6e4ud4orfv9",
    'IAM_TOKEN': "t1.9euelZqOy4maxsrKyYrOk5WRmsvIiu3rnpWay52RlYuSns_Hx8mZlYnNlZfl9PctBg1O-e9KTGS13fT3bTQKTvnvSkxktc3n9euelZrGk5jIl8_KjpSNjsmdzJaUyu_8xeuelZrGk5jIl8_KjpSNjsmdzJaUyr3rnpWamZaWmomTjs2Ry8zNm5mSzJa13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.ktILq0spKQ1aKxMBtHuVEaUkKa7PgRPJKUFkccJw_QGEyUBk0YESORBupNPnvwn_AV-IFCTEhWhQmTddQT50AQ",
    'BOT_TOKEN': '7129389249:AAHmqsgt_KN0LmufD-J3H4fht66KpkKblpQ'
}

SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселый собеседник. Общайся с пользователем на "ты" и используй юмор. '
                                            'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь. '
                                            'Изображай человека'}]
