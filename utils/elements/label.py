"""Non-interactive text element"""
from .base_element import BaseElement


class Label(BaseElement):
    """Non-interactive element, like <div>/<label>/<p> tag element"""

    @property
    def type_of(self) -> str:
        return "label"
