"Bot itself"

import logging
import telebot  # NOTE: pyTelegramBotAPI, not telebot

log = logging.getLogger(__name__)


class Bot(object):
    "Wrapper around pyTelegramBotAPI"

    def __init__(self, config):
        "Construct bot instance"
        self.config = config
        # incapsulate rather than inherit this crap
        self.bot = telebot.TeleBot(config["token"], threaded=False)

    def run(self):
        "Run bot till interrupt"
        while 1:
            try:
                self.bot.polling(timeout=3, none_stop=True)
                break  # bot.polling swallows KeyboardInterrupt to exit cleanly
            except Exception:
                log.exception("Error")
