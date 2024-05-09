import logging
import requests
from config import config
from creds import get_creds


logging.basicConfig(
    level=config['LOGGING']['level'],
    format=config['LOGGING']['format'],
    filename=config['LOGGING']['filename'],
    filemode=config['LOGGING']['filemod']
)

iam_token, folder_id = get_creds()


def tts(text):
    headers = {
        'Authorization': f'Bearer {iam_token}',
    }
    data = {
        'speed': 1,
        'emotion': 'evil',
        'text': text,
        'lang': 'ru-RU',
        'voice': 'omazh',
        'folderId': folder_id,
    }
    response = requests.post(config['SPEECH_KIT']['TTS_URL'], headers=headers, data=data)
    logging.info('TTS: text message sent')

    if response.status_code == 200:
        return True, response.content
    else:
        return False, "При запросе в SpeechKit возникла ошибка"


def stt(data):
    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])

    headers = {
        'Authorization': f'Bearer {iam_token}',
    }

    response = requests.post(
        f"{config['SPEECH_KIT']['STT_URL']}?{params}",
        headers=headers,
        data=data
    )
    logging.info('STT: voice message sent')

    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        return False, "При запросе в SpeechKit возникла ошибка"