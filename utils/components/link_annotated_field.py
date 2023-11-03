"""Component for group of elements: Input, Labels and
extra elements in label"""
import allure  # type: ignore
from playwright.sync_api import Page

from utils.elements import Link

from .field import Field


class LinkAnnotatedField(Field):
    """Class for input with label, where label contains
    both text and link element
    """

    selectors = {
        "label": "label",
        "input": "input",
        "textarea": "textarea",
        "link": "a",
    }

    def __init__(
        self,
        page: Page,
        locator: str,
        name: str,
        input_type: str = "input",
        elements_selectors_override: dict | None = None,
    ) -> None:
        super().__init__(
            page, locator, name, input_type, elements_selectors_override
        )
        self.label_link = Link(
            page,
            f"{locator} label {self.element_selectors['link']}",
            f"Link of Annotated Field {name}",
        )

    @property
    def name(self) -> str:
        return f'"{self.name_prefix}" link-annotated Field'

    def get_link_value(self, **locator_qualifiers):
        """Returns link's href"""
        return self.label_link.get_href(**locator_qualifiers)

    # --- Actions
    def click_link(self, **locator_qualifiers):
        """Clicks link in label"""
        self.log("Clicking link in label annotation")
        self.label_link.click(**locator_qualifiers)

    # --- Assertions
    def label_should_contain_link(self, **locator_qualifiers):
        """Checks that Label contains a link"""

        self.log("Check that label contains a link")
        with allure.step(
            f'Check that annotated field "{self.name}" ' "contains a link"
        ):
            self.label_link.should_be_visible(**locator_qualifiers)

    def label_link_should_have_value(self, value: str, **locator_qualifiers):
        """Checks that Label's link href is equal to given value"""

        self.log("Check that label's link have href %s", value)
        self.label_link.should_have_value(value, **locator_qualifiers)
