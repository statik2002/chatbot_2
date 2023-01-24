# Скрипты чатботов Telegram и VK c ботом помощником.

## Общее описание
Данные боты могут самостоятельно отвечать на некоторые вопросы которые указаны в файле `questions.json`.
В случе, когда бот не в состоянии ответить на введенную фразу, то он не отвечает, а просит подождать когда ответит оператор.


## Установка

Создайте виртуальное окружение командой:

```commandline
python3 -m env venv
```

Войдите в виртуальное окружение командой:
```commandline
source env/bin/activate
```

Установите зависимости командой:
```commandline
pip install -r requirements.txt
```

Создайте проект в Google Cloud по [инструкции](https://cloud.google.com/dialogflow/es/docs/quick/setup)

Создайте агента DialogFlow по [инструкции](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)

Создайте группу в VK на вкладке "Управление"

Создайте файл `.env` и внесите туда:
1. TELEGRAM_TOKEN=[Ваш TOKEN из телеграм]
2. GOOGLE_APPLICATION_CREDENTIALS=[Путь к файлу JSON ключа ]
    для создания этого файла выполните команду ```gcloud auth application-default login```
    файл будет храниться в папке (к примеру): `/.config/gcloud/application_default_credentials.json`
3. GOOGLE_CLOUD_PROJECT_ID='ваш идентификатор проекта'
   Это номер проекта после регистрации на Google Cloud
4. VK_TOKEN='Ваш токен группы в VK'

Заполните вопросами и ответами ваш DialogFlow из файла `questions.json` командой
```commandline
python create_intent.py
```

## Запуск скриптов

Для запуска Telegram бота выполните команду:
```commandline
python telegram_chatbot.py
```

Для запуска VK бота выполните команду:
```commandline
python vk_chatbot.py
```