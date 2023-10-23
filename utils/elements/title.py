"""Title (Header) element"""
from .base_element import BaseElement


class Title(BaseElement):
    """Title element, representing element of <h1-6> tag"""

    @property
    def type_of(self) -> str:
        return "title"
