import os
import random
import logging

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from utils import detect_intent_texts, authenticate_implicit_with_adc


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

        self.tg_bot.send_message(chat_id=self.chat_id, text='VK бот запущен')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def echo(event, vk_api, project_id, bot):

    session_id = event.user_id

    message = detect_intent_texts(project_id, session_id, event.text, 'ru')

    if message.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Я не могу понять ваш вопрос. Ждите оператора.',
            random_id=random.randint(1, 1000)
        )

        bot.send_message(chat_id=os.environ['CHAT_ID'], text='Пиииу пиииу кря кря!. Пользователю из VK нужна помощь!')

    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    bot = telegram.Bot(token=telegram_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, os.environ['CHAT_ID']))

    authenticate_implicit_with_adc(project_id)

    try:
        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api, project_id, bot)

    except Exception as warn:
        logger.error(f'Error {warn}.')


if __name__ == "__main__":
    main()
