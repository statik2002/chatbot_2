import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from google.cloud import dialogflow
from google.cloud import storage

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


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )

    return response.query_result.fulfillment_text

    '''
    for text in texts:
        print(text)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )

        return response.query_result.fulfillment_text
    '''


def echo(update: Update, context: CallbackContext) -> None:

    message = detect_intent_texts('pacific-hybrid-245815', 123456789, update.message.text, 'ru')

    update.message.reply_text(message)


def main() -> None:

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']

    #detect_intent_texts('pacific-hybrid-245815', 123456789, 'I know French', 'ru')

    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
