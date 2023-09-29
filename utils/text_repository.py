"""Text repository helps to read messages from .ini file.
Provides class and an instance accessing default 'messages.ini' catalog."""

import re
from configparser import ConfigParser

from constants import MESSAGES_REPOSITORY


class TextRepository:
    """Class that reads message catalog and provide methods
    to get value from it."""
    def __init__(self, file: str):
        self.parser = ConfigParser()
        self.parser.read_file(open(file, encoding="utf-8"))

    def get(self, path: str) -> str | re.Pattern:
        """Returns value from given section and key.
        If value starts from r" or r' - value will be
        compiled as regex pattern.

        Args:
            path (str): section and key name, in format:
            <section>/<key>.

        Returns:
            str|re.Pattern: message from text catalog.
        """
        section, key = path.split(' ')
        value = self.parser[section][key]

        if value.startswith('r"') or value.startswith("r'"):
            value = re.compile(value[2:-1])

        return value


messages = TextRepository(MESSAGES_REPOSITORY)
