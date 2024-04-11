#!/usr/bin/env python3
"""
Filter Logger Module
"""
import re
import logging
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
