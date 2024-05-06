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
    'MAX_USERS': '1',
    # 'MAX_SESSION': '3',
    # 'MAX_TOKEN_IN_SESSION': '1000',
    'MAX_USER_TTS_SYMBOLS': '2000',
    'MAX_TTS_SYMBOLS': '10',
    'MAX_USER_STT_BLOCKS': '1',
    'MAX_USER_GPT_TOKENS': '2000',
    'MAX_ANSWER_GPT_TOKENS': '64',
    }

config['PROMPTS'] = {
    'SYSTEM': 'Ты веселый собеседник. Общайся с пользователем на "ты" и используй юмор. '
               'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь. '
               'Изображай человека',
    # 'END': 'Напиши логическое завершение истории c неожиданной развязкой. Не добавляй пояснительный текст',
    # 'CONTINUE': 'Логически продолжи сюжет в 1-3 предложения, держи интригу. Не добавляй пояснительный текст'
}

config['MAIN'] = {
    'DB_FILE': 'messages.db'
}

config['CREDENTIALS'] = {
    'FOLDER_ID': 'b1gmco3nm6e4ud4orfv9',
    'IAM_TOKEN': 't1.9euelZqVm5WZns_PkM-Pjo6SyMnPx-3rnpWay52RlYuSns_Hx8mZlYnNlZfl9Pc4FhtO-e8FNyXv3fT3eEQYTvnvBTcl783n9euelZrGnMuVkMiOkJuVzJeKlorMx-_8xeuelZrGnMuVkMiOkJuVzJeKlorMx73rnpWayZvGj47HyMrOnM7PnpKUj5e13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.MMmLv58WWoucKUC3K1FsceiRkOn1LmBe9W6sXsTh-51XlhrK0G7l_e0uZtFtLapC6HkFE4zudjzsW-yOLoCFBQ',
    'BOT_TOKEN': '7129389249:AAHmqsgt_KN0LmufD-J3H4fht66KpkKblpQ'
}