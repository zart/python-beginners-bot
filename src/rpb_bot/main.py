"Main entry"

import os

# init sentry as early as possible, but only when requested with env var
if "SENTRY_SDK" in os.environ:
    try:
        __import__("sentry_sdk").init(os.getenv("SENTRY_SDK"))
    except ImportError:
        pass

import json
from logging import basicConfig, getLogger
from logging.config import fileConfig, dictConfig
from .config import get_config

log = getLogger(__name__)


def run():
    # configuration
    config = get_config()

    # init logging
    log_path = config["log_config"] or config["config"]
    try:
        if log_path:
            if log_path.endswith(".json"):
                with open(log_path) as fp:
                    dictConfig(json.load(fp))
                log.debug("Configured logging from JSON: %s", log_path)
            else:
                fileConfig(log_path)
                log.debug("Configured logging from INI: %s", log_path)
    except Exception:
        basicConfig("%(loglevel)-5s [%(name)s] %(message)s")
        log.debug("Falling back on basic logging config", exc_info=True)

    # instantiate the bot
    # check connection to database and redis
    # start the bot if everything is fine
