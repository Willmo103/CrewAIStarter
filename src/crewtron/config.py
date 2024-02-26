import datetime as dt
import json
import os
import time
from logging import Logger
from logging.config import dictConfig

import log_handlers  # noqa

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

_conf_path: str = os.path.join(PROJECT_ROOT, "config.json")
_config: dict = {}
_log: Logger = None


def get_config():
    global _config
    if not _config:
        with open(_conf_path, "r") as file:
            return json.load(file)
    else:
        return _config


def get_api_key(key):
    return get_config().get("apiKeys").get(key, None)


def get_connection_string(key):
    return get_config().get("connectionStrings").get(key, None)


def get(key):
    return get_config().get(key, None)


def get_base_url():
    return get_config().get("OllamaBaseUrl", None)


def init_logger() -> Logger:
    global _log
    if _log:
        return _log
    dictConfig(get_config()["loggingConfig"])
    _log = Logger("app_logger")
    return _log.getChild(__name__)


# a wrapper to log the time and result of each function call


def log_time(func) -> callable:
    def wrapper(*args, **kwargs):
        __logger = init_logger().getChild(func.__name__)
        start = dt.datetime.now()
        result = None
        try:
            result = func(*args, **kwargs)
            end = dt.datetime.now()
            __logger.debug(
                f"{func.__name__} executed in {end - start}\nResult: {result.__str__() if result else ''}"
            )
        except Exception as e:
            end = dt.datetime.now()
            __logger.error(
                f"{func.__name__} failed in {end - start}\nError: {e}"
            )
        return result

    return wrapper


@log_time
def test_log_time():
    print("Test function executed.")
    time.sleep(3)
    return get_config()


if __name__ == "__main__":
    __log = init_logger()
    __log.info(f"Testing the config module.")
    print(PROJECT_ROOT, APP_ROOT)
    test_log_time()
