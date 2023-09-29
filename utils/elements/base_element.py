"""Basic component class"""
from abc import ABC, abstractmethod

import allure
from playwright.sync_api import Locator, Page, expect


class BaseElement(ABC):
    """Base class for HTML element"""
    def __init__(self, page: Page, locator: str, name: str) -> None:
        self.page = page
        self.name = name
        self.locator = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        """Return name of the element's type."""
        return 'element'

    def get_locator(self, **locator_qualifiers) -> Locator:
        """Returns qalified locator of the element.

        Returns:
            Locator: locator object.
        """
        locator = self.locator.format(**locator_qualifiers)
        return self.page.locator(locator)

    # --- Actions
    def click(self, **locator_qualifiers) -> None:
        """Clicks on element."""
        with allure.step(f'Clicking {self.type_of} with name "{self.name}"'):
            locator = self.get_locator(**locator_qualifiers)
            locator.click()

    # --- Assertions
    def should_be_visible(self, **locator_qualifiers) -> None:
        """Checks that element is visible."""
        with allure.step(f'{self.type_of.capitalize()} with name '
                         f'"{self.name}" should be visible'):
            expect(self.get_locator(**locator_qualifiers)).to_be_visible()

    def should_have_text(self, text: str, **locator_qualifiers) -> None:
        """Checks that element have given text."""
        with allure.step(f'{self.type_of.capitalize()} with name '
                         f'"{self.name}" should have text "{text}"'):
            expect(self.get_locator(**locator_qualifiers)).to_have_text(text)
