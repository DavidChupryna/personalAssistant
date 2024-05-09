import logging
import requests
from config import config, LOGS
from creds import get_creds


logging.basicConfig(filename=LOGS, level=logging.INFO,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

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