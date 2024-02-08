#!/usr/bin/env python3
""" Logs obfuscation module """
from typing import List
import logging
import mysql.connector as connector
import os
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """" Changes log messages by obfuscating sensitive
         information.
         Args:
            fields: a list of strings representing all
                    fields to obfuscate
            redaction: a string representing by what
                       the field will be obfuscated.
            message: a string representing the log line
            separator: a string representing by which
                       character is separating all fields
                       in the log line message.
    """
    for field in fields:
        message = re.sub(r"{}=.*?{}".format(field, separator),
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Custom formatting of log messages """
        return filter_datum(fields=self.fields,
                            redaction=RedactingFormatter.REDACTION,
                            message=super().format(record),
                            separator=RedactingFormatter.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Creates and returns a logger object with:
        1. A stream handler.
        2. Logging level set to INFO.
        3. Redacting formatter.
    """
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connector.MySQLConnection:
    """ Establishes a database connection """
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    connection = connector.connect(host=host, database=database,
                                   user=username, password=password)
    return connection


def main() -> None:
    """ Retrieves data from database tables and
        logs its while obfuscating sensitive fields.
    """
    db_connection = get_db()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = ';'.join(["{}={}".format(key, value)
                            for key, value in row.items()])
        logger.info(message)
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()