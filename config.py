import configparser

HOME_DIR = '/home/student/personalAssistant'
LOGS = f'{HOME_DIR}/logs.txt'
DB_FILE = f'{HOME_DIR}/messages.db'
AUDIO_FILE = f'{HOME_DIR}/output.ogg'

IAM_TOKEN_PATH = f'{HOME_DIR}/creds/iam_token.txt'
FOLDER_ID_PATH = f'{HOME_DIR}/creds/folder_id.txt'
BOT_TOKEN_PATH = f'{HOME_DIR}/creds/bot_token.txt'

config = configparser.ConfigParser()

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
    'MAX_USER_TTS_SYMBOLS': '4000',
    'MAX_TTS_SYMBOLS': '500',
    'MAX_USER_STT_BLOCKS': '15',
    'MAX_USER_GPT_TOKENS': '2000',
    'MAX_ANSWER_GPT_TOKENS': '64',
    'COUNT_LAST_MESSAGE': '4'
}

SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселый собеседник. Общайся с пользователем на "ты" и используй юмор. '
                                            'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь. '
                                            'Изображай человека'}]
