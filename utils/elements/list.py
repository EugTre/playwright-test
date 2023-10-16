"""List item element"""

import allure
from playwright.sync_api import expect

from .base_element import BaseElement


class List(BaseElement):
    """List element, representing group of <li> tag elements"""
    @property
    def type_of(self) -> str:
        return 'list'

    def should_have_items(self, items_text: list[str] | tuple[str],
                          **locator_qualifiers) -> None:
        """Checks that list's items are equal to given list of names"""
        with allure.step(f'{self.type_of.capitalize()} should have items '
                         f'{items_text}'):
            expect(self.get_locator(**locator_qualifiers))\
                .to_have_text(items_text)
