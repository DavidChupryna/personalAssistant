import logging
import requests
from config import config, SYSTEM_PROMPT

logging.basicConfig(
    level=config['LOGGING']['level'],
    format=config['LOGGING']['format'],
    filename=config['LOGGING']['filename'],
    filemode=config['LOGGING']['filemod']
)
iam_token = config['CREDENTIALS']['IAM_TOKEN']
folder_id = config['CREDENTIALS']['FOLDER_ID']


def count_gpt_tokens(messages):
    url = config['GPT']['TOKENIZE_URL']
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages):
    url = config['GPT']['URL']
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": int(config['LIMITS']['MAX_ANSWER_GPT_TOKENS'])
        },
        "messages": SYSTEM_PROMPT + messages
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        logging.info('GPT: request sent!')
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None

        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer

    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT", None

