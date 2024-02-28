import datetime as dt
import json
import os
from logging import Logger
from logging.config import dictConfig
import uuid
import log_handlers  # noqa


class Config:
    def __init__(self):
        self._PROCESS_UUID = uuid.uuid4()
        self.PROJECT_ROOT = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.CACHE = os.path.join(self.PROJECT_ROOT, "cache")
        self.TMP = os.path.join(self.PROJECT_ROOT, "tmp")
        self.DOCKER = os.path.join(self.PROJECT_ROOT, "docker")
        self.LOGS = os.path.join(self.PROJECT_ROOT, "logs")

        for d in [self.CACHE, self.TMP, self.DOCKER, self.LOGS]:
            if not os.path.exists(d):
                os.makedirs(d)

        with open(os.path.join(self.PROJECT_ROOT, "config.json")) as file:
            f = json.load(file)
            self.__api_keys = f.get("APIKeys", {})
            self.__connection_strings = f.get("connectionStrings", {})
            self.__log_config = f.get("loggingConfig", {})
            self.__config = f
        self._LOG: Logger = self.get_logger()

    def get_api_key(self, key):
        return self.__api_keys.get(key, None)

    def get_connection_string(self, key):
        return self.__connection_strings.get(key, None)

    def get_item(self, key):
        return self.__config.get(key, None)

    def get_base_url(self):
        return self.__config.get("OllamaBaseUrl", None)

    def get_logger(self) -> Logger:
        dictConfig(self.__log_config)
        self._LOG = Logger(f"app_logger {self._PROCESS_UUID}")
        return self._LOG.getChild(__name__)

    # a wrapper to log the time and result of each function call


config = Config()


def log_v(logger_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            __logger = config.get_logger(logger_name).getChild(func.__name__)
            start = dt.datetime.now()
            result = None
            try:
                result = func(*args, **kwargs)
                end = dt.datetime.now()
                fmtime = f"{(end - start).total_seconds()} seconds"
                __logger.debug(
                    f"{func.__name__} executed in {fmtime}\nResult: {result.__str__() if result else ''}"
                )
            except Exception as e:
                end = dt.datetime.now()
                __logger.error(f"{func.__name__} failed in {end - start}\nError: {e}")
            return result
        return wrapper
    return decorator


if __name__ == "__main__":
    print(config.get_base_url())
    print(config.get_api_key("test"))
    print(config.get_connection_string("test"))
    print(config.get_item("OllamaBaseUrl"))
    print(config.get_logger())
    print(config.log_v(lambda x: x)(5))
