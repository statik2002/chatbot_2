import json
import os

from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow
from dotenv import load_dotenv


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main() -> None:
    load_dotenv()
    project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    with open('questions.json', 'r') as intents_file:
        intents = json.load(intents_file)

    for intent, phrases in intents.items():

        try:
            create_intent(
                project_id,
                intent,
                phrases['questions'],
                phrases['answer']
            )
        except InvalidArgument as e:
            print(f'Warning! - {e.message}')


if __name__ == '__main__':
    main()
