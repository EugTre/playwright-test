"""Non-interactive element"""
from .base_element import BaseElement


class Banner(BaseElement):
    """Non-interactive element, like <div> tag element"""
    @property
    def type_of(self) -> str:
        return 'banner'
