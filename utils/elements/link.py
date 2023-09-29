"""Link element class"""
from .base_element import BaseElement


class Link(BaseElement):
    """Link element class, representing element of <a> tag """
    @property
    def type_of(self) -> str:
        return 'link'
