import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from create_api_key import authenticate_implicit_with_adc
from utils import detect_intent_texts


def echo(event, vk_api):

    message = detect_intent_texts('pacific-hybrid-245815', 123456789, event.text, 'ru')

    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )


def main():
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    authenticate_implicit_with_adc(project_id)

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == "__main__":
    main()
