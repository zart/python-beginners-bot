"Bot itself"

import telebot  # NOTE: pyTelegramBotAPI, not telebot


def get_bot(config):
    "Bot factory"

    bot = telebot.TeleBot(config['token'], threaded=False)

    return bot
