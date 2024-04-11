#!/usr/bin/env python3
"""
Filter Logger Module
"""
import os
import re
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Returns the log message obfuscated

    Keyword arguments:
    fields -- a list of strings representing all fields to obfuscate
    redaction -- a string representing by what the field will be obfuscated
    message -- a string representing the log line
    separator -- a string representing by which character is separating
    all fields in the log line (message)
    Return: log message obfuscated
    """
    return re.sub(
        "({})=.*?(?={})".format("|".join(fields), separator),
        r"\1={}".format(redaction),
        message
    )


def get_logger() -> logging.Logger:
    """Returns a logger for the user data"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connection to a MySQL database"""
    conn = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return conn


def main() -> None:
    """Retrieves all rows in the users table and
    display each row under a filtered format"""

    conn = get_db()
    user_logger = get_logger()

    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    query = "SELECT {} FROM users".format(fields)
    columns = fields.split(",")
    with conn.cursor() as cursor:
        cursor.execute(query)
        users = cursor.fetchall()

        for user in users:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, user),
            )
            message = '{};'.format('; '.join(list(record)))
            user_logger.info(message)
    conn.close()


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
        """Converts a LogRecord to an output string"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super().format(record)


if __name__ == "__main__":
    main()
