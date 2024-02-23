import json
import logging
import os
from logging import Logger
from logging.config import dictConfig

import psycopg2

# from psycopg2.extras import DictCursor


class Config:
    def __init__(self):
        self.package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.package_root, "config.json")
        self.config = self.read_config()
        self.logger = self.init_logger()

    def read_config(self):
        with open(self.config_file) as file:
            return json.load(file)

    def init_logger(self):
        dictConfig(self.config["loggingConfig"])
        return Logger("app_logger")

    def get(self, key):
        return self.config.get(key, None)

    def get_api_key(self, key):
        return self.config.get("apiKeys").get(key, None)

    def get_connection_string(self, key):
        return self.config.get("connectionStrings").get(key, None)

    @classmethod
    def init_config(cls):
        return Config()


class PostgresHandler(logging.Handler):
    def __init__(self, dbname, user, password, host):
        logging.Handler.__init__(self)
        self.connection_string = (
            f"dbname='{dbname}' user='{user}' password='{password}' host='{host}'"
        )
        self.conn = psycopg2.connect(self.connection_string)
        self.create_table()

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            levelname TEXT,
            levelno INTEGER,
            pathname TEXT,
            filename TEXT,
            module TEXT,
            lineno INTEGER,
            funcName TEXT,
            message TEXT,
            exc_info TEXT,
            stack_info TEXT
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            self.conn.commit()

    def emit(self, record):
        insert_sql = """
        INSERT INTO logs (name, levelname, levelno, pathname, filename, module, lineno, funcName, message, exc_info, stack_info)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        self.format(
            record
        )  # Ensure record attributes like exc_info are formatted into strings
        exc_info = self.formatException(record.exc_info) if record.exc_info else None
        stack_info = self.formatStack(record.stack_info) if record.stack_info else None

        with self.conn.cursor() as cursor:
            cursor.execute(
                insert_sql,
                (
                    record.name,
                    record.levelname,
                    record.levelno,
                    record.pathname,
                    record.filename,
                    record.module,
                    record.lineno,
                    record.funcName,
                    record.getMessage(),
                    exc_info,
                    stack_info,
                ),
            )
            self.conn.commit()

    def close(self):
        self.conn.close()
        logging.Handler.close(self)
