"Bot settings"

import os, argparse
from configparser import RawConfigParser
from .errors import ConfigError

DESCRIPTION = "Telegram bot"

NO_META = """\
Пожалуйста, не задавайте мета-вопросов в чате!
Мета-вопрос - это вопрос, который подразумевает другие вопросы.
http://nometa.xyz/
"""

# default values
DEFAULTS = dict(
    config="bot.ini",
    log_config=None,
    database_url=None,
    redis_url=None,
    debug=False,
    git_token=None,
    token=None,
    chat_name="@ru_python_beginners",
    max_file_size=1000000,
    extensions=[".py", ".txt", ".json"],
    paste_url="https://api.github.com/gists",
    nometa=NO_META,
    whitelist_channels=[-1001120424883],  # @best_of_ru_python
    report_threshold=2,
    spammer_timeout=10,
    ro_duration=60,
    # ro_levels={1: 5, 2: 30, 3: 120, 4: "ban"},
    # unreachable_exc=r"<Response [403]>",
)


def get_parser(*args, version=None, **kwargs):
    "Factory for default cmdline parser"

    parser = argparse.ArgumentParser(*args, **kwargs, description=DESCRIPTION)

    # helpers
    arg = parser.add_argument
    arg0 = lambda *a, **k: arg(*a, **k, help=argparse.SUPPRESS)

    # add --version if provided
    if version:
        arg("-V", "--version", action="version", version=version)

    arg("--config", default="bot.ini", help="config file [%(default)s]")

    # TODO: convert to real arguments instead of placeholders
    arg0("--log-config")
    arg0("--chat-name")
    arg0("--extensions")
    arg0("--max-file-size")
    arg0("--database-url")
    arg0("--redis-url")
    arg0("--paste-url")
    arg0("--debug", action="store_true")
    arg0("--nometa")
    arg0("--whitelist-channels", action="append", type=int)
    arg0("--report-threshold", type=int, default=2)
    arg0("--spammer-timeout", type=int, default=10)
    arg0("--ro-duration", type=int, default=60)
    # ro_levels = {1: 5, 2: 30, 3: 120, 4: "ban"}
    # unreachable_exc = r"<Response [403]>"
    arg0("--git-token")
    arg0("--token")
    parser.set_defaults(**DEFAULTS)

    return parser


class DEFAULT(object):
    "Sentinel value for config functions"
    __repr__ = __str__ = lambda self: "<DEFAULT>"


DEFAULT = DEFAULT()


def get_config_envvars(prefix=None, env=os.environ):
    "Returns key/values from dict env where keys start with a prefix"

    if prefix is None:  # special case
        return {}

    d = len(prefix)
    envvars = {k[d:].lower(): env[k] for k in env if k.startswith(prefix)}

    return envvars


def get_config_ini(path=None, section="bot", parser_class=RawConfigParser):
    "Read configuration from ini file"

    if path is None:  # special case
        return {}

    cfg = parser_class()
    if not cfg.read(path):
        raise ConfigError("Failed to read configuration", path)
    ini = dict(cfg.items(section))

    return ini


def get_config_cmdline(parser=None, defaults=None):
    "Read configuration from ini file"

    if parser is None:  # special case
        return {}

    if parser is DEFAULT:
        parser = get_parser()

    if defaults:
        parser.set_defaults(**defaults)

    args = vars(parser.parse_args())

    return args


def get_config(
    path=None,
    section="bot",
    parser=DEFAULT,
    envprefix="RPB_BOT_",
    environ=os.environ,
    defaults=DEFAULTS,
):
    "Combine configuration from multiple sources"

    config = dict.fromkeys(defaults, DEFAULT)
    cmd = get_config_cmdline(parser, config)
    cfg = cmd["config"]
    path = cfg if cfg is not DEFAULT else path or defaults["config"]
    ini = get_config_ini(path, section)
    env = get_config_envvars(envprefix, environ)

    # merge sources by priority and unknown entries are ignored
    for key in defaults:
        if config.get(key, DEFAULT) is DEFAULT:
            for src in (cmd, ini, env, defaults):
                if src.get(key, DEFAULT) is not DEFAULT:
                    config[key] = src[key]
                    break

    # TODO: fix types. ini and envvars return Mapping[str, str], cmdline doesnt

    return config
