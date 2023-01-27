import logging
import os
from functools import partial

import telegram
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from utils import detect_intent_texts, TelegramLogsHandler

logger = logging.getLogger(__file__)


def message_answer(
        update: Update,
        context: CallbackContext,
        project_id,
        chat_id) -> None:

    session_id = update.message.from_user.id

    message = detect_intent_texts(
        project_id,
        session_id,
        update.message.text,
        'ru'
    )

    update.message.reply_text(message.fulfillment_text)


def error_handler(update, context):
    logger.error(msg='Ошибка при работе скрипта: ', exc_info=context.error)


def main() -> None:

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    service_bot = telegram.Bot(token=telegram_token)
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(service_bot, chat_id))

    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            partial(message_answer, project_id=project_id, chat_id=chat_id)
        )
    )
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
