import datetime as dt
import logging
import os

import psycopg2

_logs = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs"
)


class PostgresHandler(logging.Handler):
    def __init__(self, dbname, user, password, host, port):
        logging.Handler.__init__(self)
        self.connection_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"
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


class CustomFileHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.filename = os.path.join(
            _logs, dt.datetime.now().strftime("%Y-%m-%d") + ".log"
        )

    def emit(self, record):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write("\r")
        with open(self.filename, "a") as file:
            file.write(self.format(record) + "\n")

    def close(self):
        logging.Handler.close(self)
