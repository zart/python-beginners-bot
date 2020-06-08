"Main entry"

import os

# init sentry as early as possible, but only when requested with env var
if "SENTRY_SDK" in os.environ:
    try:
        __import__("sentry_sdk").init(os.getenv("SENTRY_SDK"))
    except ImportError:
        pass

from .config import get_config


def run():
    config = get_config()
    print(config)

    # init logging
    # instantiate the bot
    # check connection to database and redis
    # start the bot if everything is fine
