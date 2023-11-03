"""Link element class"""
import allure  # type: ignore
from playwright.sync_api import expect

from .base_element import BaseElement


class Link(BaseElement):
    """Link element class, representing element of <a> tag"""

    @property
    def type_of(self) -> str:
        return "link"

    def get_href(self, **locator_qualifiers):
        """Retuns link's href value"""
        locator = self.get_locator(**locator_qualifiers)
        href = locator.get_attribute("href")
        self.log("Link's retrieved href: %s (%s)", href, locator)
        return href

    def should_have_value(self, value, **locator_qualifiers):
        """Checks that link href equals to given value.

        Args:
            value (str): link value.
        """
        locator = self.get_locator(**locator_qualifiers)
        self.log("Check link's href value to match %s (%s)", value, locator)
        with allure.step(
            f"{self.type_of.capitalize()} with name "
            f'"{self.name}" should have href value "{value}"'
        ):
            expect(locator).to_have_attribute("href", value)
