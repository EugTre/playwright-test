"""List item element"""
from .base_element import BaseElement


class ListItem(BaseElement):
    """List item element, representing element of <li> tag """
    @property
    def type_of(self) -> str:
        return 'list item'
