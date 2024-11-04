# Telegram Defender

![aiogram](https://img.shields.io/badge/python-v3.12.7-blue.svg?logo=python&logoColor=yellow) ![aiogram](https://img.shields.io/badge/aiogram-v3-blue.svg?logo=telegram) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

This bot has a wide range of capabilities, in addition to the usual functions such as mute and ban, there are other features, unmute and unban. The bot also implements a warning system using PostgreSQL+SQLalchemy. Special middleware for greeting and farewell to the user have also been implemented. There is also a message filter for links and bad words based on NLP Spacy. There is also a system for checking messages for flood using NLP Spacy and Redis.

## Features

The bot provides the following features:

- Mute and Unmute users
- Ban and Unban users
- Issue warnings to users
- Filter messages
- Say hello and goodbye to users

## Commands

The bot has several commands that can be used to access its features:

- `/help`: Sends a Handlers Guide
- `/mute`:
- `/unmute`:
- `/ban`:
- `/unban`:
- `/warn`:
- `/message_id`:  

## Requirements

- **Python** v3.12.7
- **aiogram** v3
- **SQLAlchemy** v2
- **asyncpg** v0.27
- **Alembic** v1
- **psycopg2** v2
- **spaCy** v3
- **Redis** v5
- **python-dotenv** v1

## Installation

To get started with this bot, follow these steps:

## Common Steps

1. **Clone this repository** to your local machine:

    ```bash
    git clone https://github.com/serafimiumroadtojunior/defense_moderator_v2
    ```

2. **Create a new bot** on Telegram by talking to [BotFather](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) and obtain the API token.

3. **Rename the file** `.env.dist` to `.env` and replace the placeholders with the required data.

## Running on Windows

Follow these steps to run the bot on Windows:

1. **Install [Poetry](https://python-poetry.org/docs/#installation)** if you haven't done so already.

2. **Create a virtual environment, activate it, and install the required dependencies**:

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate
    poetry install
    ```

3. **Run the bot**:

    ```powershell
    poetry run python bot.py
    ```

## Running with Docker

To run the bot using Docker, follow these steps:

1. **Ensure you have Docker and Docker Compose installed**. If not, follow the instructions on the [official Docker website](https://docs.docker.com/get-docker/) to install them.

2. **Navigate to the project directory** where your `docker-compose.yml` file is located.

3. **Build and start the Docker containers**:

    ```bash
    docker-compose up --build
    ```

4. **Verify that the bot is running**. You should see logs in the terminal indicating that the bot is active and ready to respond.
