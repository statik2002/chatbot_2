import os

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from create_api_key import authenticate_implicit_with_adc


def main() -> None:
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    authenticate_implicit_with_adc(project_id)

    vk_session = vk_api.VkApi(token=vk_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()