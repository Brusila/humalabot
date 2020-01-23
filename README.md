# humalabot

Telegram bot for tracking alcohol consumption.

## About

- This is an exercise project in progress.
- The bot is not online (most of the time).
- The program uses [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) wrapper.

## Setup

- Create the bot on Telegram and get the bot token with [BotFather](https://core.telegram.org/bots/faq#how-do-i-create-a-bot).
- Create a file named "token.txt", copy-paste the token in the file and place the file in the /program/ folder.
- Use the command 'pip install -r requirements.txt' to install the requirements.

## Using

Command | Info
--------|------
/aloita [gender] [weight] | Add the needed information about yourself
/juo [drink] | Add a drink after you have finished it
/promillet | Shows your current drunkenness level
/maksimit | Shows your highest drunkenness level
/juomalista | Shows all available drinks
