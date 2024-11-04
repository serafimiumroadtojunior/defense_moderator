# Telegram Defender

![aiogram](https://img.shields.io/badge/python-v3.12.7-blue.svg?logo=python&logoColor=yellow) ![aiogram](https://img.shields.io/badge/aiogram-v3-blue.svg?logo=telegram) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

This bot has a wide range of capabilities, in addition to the usual functions such as mute and ban, there are other features, unmut and unban. The bot also implements a warning system using PostgreSQL+SQLalchemy. Special middleware for greeting and farewell to the user have also been implemented. There is also a message filter for links and bad words based on NLP Spacy. There is also a system for checking messages for flood using NLP Spacy and Redis.

## Features

The bot provides the following features:

-
-

## Commands

The bot has several commands that can be used to access its features:

- `/start`: Sends a ...
- `/help`: Sends a ...

## Requirements

- Python v3.12.7
- aiogram v3
- dotenv v1

## Installation

To get started with this bot, follow these steps:

- Clone this repository to your local machine.

    ```
    $ git clone [source]
    ```

- Create a virtual environment, activate it and install required dependencies.

    ```
    $ python3.10 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements/local.txt
    ```

- Create a new bot on Telegram by talking to the BotFather, and [obtain the API token](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token).

- Rename the file `.env.dist` to `.env` and replace the placeholders with required data.

- Run the bot using `python bot.py`.
