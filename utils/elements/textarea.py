"""Input elements class"""
from .input import Input


class Textarea(Input):
    """Class for Input tag element"""

    @property
    def type_of(self) -> str:
        return "textarea"
