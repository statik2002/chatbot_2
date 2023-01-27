import os
import random
import logging

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from utils import detect_intent_texts, TelegramLogsHandler

logger = logging.getLogger(__name__)


def answer_message(event, vk_api, project_id, bot, chat_id):

    session_id = event.user_id

    message = detect_intent_texts(project_id, session_id, event.text, 'ru')

    if not message.intent.is_fallback:
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
    chat_id = os.environ['CHAT_ID']

    bot = telegram.Bot(token=telegram_token)

    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_message(event, vk_api, project_id, bot, chat_id)


if __name__ == "__main__":
    main()
