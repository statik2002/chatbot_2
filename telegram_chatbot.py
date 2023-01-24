import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from utils import detect_intent_texts, authenticate_implicit_with_adc

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:

    session_id = update.message.from_user.id

    message = detect_intent_texts(os.environ['GOOGLE_CLOUD_PROJECT_ID'], session_id, update.message.text, 'ru')

    if message.intent.is_fallback:
        update.message.reply_text('Я не могу понять ваш вопрос. Ждите ответ оператора.')
    else:
        update.message.reply_text(message.fulfillment_text)


def main() -> None:

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    authenticate_implicit_with_adc(project_id)

    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
