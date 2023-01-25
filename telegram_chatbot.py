import logging
import os
import traceback
from functools import partial

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackContext

from utils import detect_intent_texts


logger = logging.getLogger(__file__)


def message_answer(update: Update, context: CallbackContext, project_id, chat_id) -> None:

    session_id = update.message.from_user.id

    message = detect_intent_texts(
        project_id,
        session_id,
        update.message.text,
        'ru'
    )

    x = 100 / 0

    if message.intent.is_fallback:
        context.bot.send_message(
            chat_id,
            text='Пиииу пиииу кря кря!. Пользователю из Telegram нужна помощь!'
        )

    update.message.reply_text(message.fulfillment_text)


def error_handler(update, context, chat_id):
    logger.error(msg='Ошибка при работе скрипта: ', exc_info=context.error)
    context.bot.send_message(chat_id, text=traceback.format_exception())


def main() -> None:

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            partial(message_answer, project_id=project_id, chat_id=chat_id)
        )
    )
    dispatcher.add_error_handler(partial(error_handler, chat_id=chat_id))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
