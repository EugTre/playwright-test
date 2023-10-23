"""List item element"""

import allure
from playwright.sync_api import Locator, expect

from .base_element import BaseElement

SELECT_OPTIONS_TEXT_VALUE_JS_SNIPPET = """node => {
        options = []
        for (let i = 0; i < node.length; ++i) {
            options.push([
                node.options[i].text,
                node.options[i].value
            ])
        }
        return options
    }"""


class Select(BaseElement):
    """Select element, representing group of <select> tag element"""

    @property
    def type_of(self) -> str:
        return "dropdown"

    def get_options(self, **locator_qualifiers) -> Locator:
        """Returns locator to dropdown's items"""
        return self.get_locator(**locator_qualifiers).locator("option")

    def get_option_names(self, **locator_qualifiers) -> list[tuple[str, str]]:
        """Returns options as list of names"""
        return self.get_options(**locator_qualifiers).all_text_contents()

    def get_options_data(self, **locator_qualifiers) -> list[tuple[str, str]]:
        """Returns tuple of options values and names"""
        return self.get_locator(**locator_qualifiers).evaluate(
            SELECT_OPTIONS_TEXT_VALUE_JS_SNIPPET
        )

    def select_option(
        self,
        value: str | None = None,
        label: str | None = None,
        **locator_qualifiers,
    ):
        """Selects option by given value or by given label"""
        locator = self.get_locator(**locator_qualifiers)

        if value is not None:
            return locator.select_option(value=value)

        if label is not None:
            return locator.select_option(label=label)

        return None

    def should_have_size_of(self, size: int, **locator_qualifiers) -> None:
        """Checks that list contains exact number of elements"""
        with allure.step(
            f"{self.type_of.capitalize()} should have " f"{size} items"
        ):
            expect(self.get_options(**locator_qualifiers)).to_have_count(size)
