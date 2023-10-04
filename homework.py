import logging
import os

import datetime
import time

import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

URL = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'

HOMEWORK_VERDICTS = {'reviewing': 'работа взята в ревью',
                     'approved': 'ревью успешно пройдено',
                     'rejected': 'в работе есть ошибки, нужно поправить'}

date_start = int(datetime.datetime(2021, 8, 1).timestamp())

logging.basicConfig(
    level=logging.DEBUG,
    filename='bot.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

def check_tokens():
    """Checking the availability of the environment that is necessary for the programs to work
    all valid - True else False"""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])

def get_api_answer(timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': timestamp}
    response = requests.get(URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.critical(f'API request error. Not all environmental variables available')
        raise Exception(f'API request error. Not all environmental variables available')

def check_response(response):
    """Checks the correctness of the API answer: json format; keys: homeworks and current_date"""
    keys = ['homeworks', 'current_date']
    if len(response) == 0:
        logging.error('Empty response')
        raise Exception(f'Empty response')
    else:
        if not isinstance(response, dict):
            logging.error(f'API response format error: response is not a dictionary')
            raise Exception(f'API response format error: response is not a dictionary')

    for key in keys:
        if response.get(key) == None:
            logging.error(f'API response format error: no keyword "{key}"')
            raise Exception(f'API response format error: no keyword "{key}"')

    if not isinstance(response.get('homeworks'), list):
        logging.error(f'API response format error: homeworks is not a list')
        raise Exception(f'API response format error: homeworks is not a list')

    return response

def parse_status(response):
    """Shows homework status in dictionary homework: status"""
    homework_statuses = {}
    homeworks = response.get('homeworks')
    if homeworks:
        for homework in homeworks:
            status = homework.get('status')
            if status in HOMEWORK_VERDICTS.keys():
                homework_statuses[homework.get('homework_name')] = status
            else:
                logging.error(f'Unknown homework status')
                raise Exception(f'Unknown homework status: {status}.')
        return homework_statuses

def send_message(bot, text):
    """Send message to telegram chat"""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text)
        logging.debug(f'Message is sent: {text}')
    except Exception as error:
        logging.error(f'Message is not sent: {error}')
        raise Exception(f'Message is not sent: {error}')

def main():
    logging.debug('Telegram bot launch')
    bot = Bot(token=TELEGRAM_TOKEN)
    if check_tokens():
        current_status = parse_status(check_response(get_api_answer(date_start)))
        send_message(bot,
                     f'Your homeworks have the following statuses: {current_status}. '
                     f'We will notify you if there are changes')
        while True:
            response = check_response(get_api_answer(date_start))
            new_statuses = parse_status(response)
            for homework in new_statuses:
                status = new_statuses.get(homework)
                if status != current_status.get(homework):
                    send_message(bot, f'New status for {homework}: {status}')

            time.sleep(60)


if __name__ == '__main__':
    main()



