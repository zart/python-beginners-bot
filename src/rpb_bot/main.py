"Main entry"
# TODO: init sentry as early as possible

from .config import get_config

def run():
    config = get_config()
    print(config)

    # init logging
    # instantiate the bot
    # check connection to database and redis
    # start the bot if everything is fine
