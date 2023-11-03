"""Basic component class"""
import logging
from abc import ABC, abstractmethod

import allure  # type: ignore
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
        return "element"

    def log(self, msg: str, *args, level: int = logging.DEBUG):
        """Logs message"""
        logging.log(
            level, f"[Element: {self.name} {self.type_of}] {msg}", *args
        )

    def get_locator(self, **locator_qualifiers) -> Locator:
        """Returns qalified locator of the element.

        Returns:
            Locator: locator object.
        """
        locator = self.page.locator(self.locator.format(**locator_qualifiers))
        self.log("Locator found (%s)", locator)
        return locator

    def get_first(self,  **locator_qualifiers) -> Locator:
        """Returns Locator by getting 'first' property of
        the element locator"""
        return self.get_locator(**locator_qualifiers).first

    def get_last(self, **locator_qualifiers) -> Locator:
        """Returns Locator by getting 'last' property of
        the element locator"""
        return self.get_locator(**locator_qualifiers).last

    # --- Actions
    def click(self, **locator_qualifiers) -> None:
        """Clicks on element."""
        with allure.step(f'Clicking {self.type_of} with name "{self.name}"'):
            locator = self.get_locator(**locator_qualifiers)
            self.log("Clicking element (%s)", locator)
            locator.click()

    # --- Assertions
    def should_be_visible(self, **locator_qualifiers) -> None:
        """Checks that element is visible."""
        locator = self.get_locator(**locator_qualifiers)
        self.log("Checking element to be visible (%s)", locator)
        with allure.step(
            f"{self.type_of.capitalize()} with name "
            f'"{self.name}" should be visible'
        ):
            expect(locator).to_be_visible()

    def should_have_text(self, text: str, **locator_qualifiers) -> None:
        """Checks that element have given text."""
        locator = self.get_locator(**locator_qualifiers)
        self.log('Checking element to have text "%s" (%s)', text, locator)
        with allure.step(
            f"{self.type_of.capitalize()} with name "
            f'"{self.name}" should have text "{text}"'
        ):
            expect(locator).to_have_text(text)
