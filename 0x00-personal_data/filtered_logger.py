#!/usr/bin/env python3
"""
Filter Logger Module
"""
import re
from typing import List


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
