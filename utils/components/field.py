"""Input elements class"""
from copy import copy
from logging import DEBUG

from playwright.sync_api import Page

from utils.elements import Input, Label, Textarea

from .base_component import BaseComponent


class Field(BaseComponent):
    """Class for group of Label and Input elements
    nested in specific locator
    """

    selectors = {"label": "label", "input": "input", "textarea": "textarea"}

    def __init__(
        self,
        page: Page,
        locator: str,
        name: str,
        input_type: str = "input",
        elements_selectors_override: dict = None,
    ) -> None:
        """Instnatiate Field component object.

        Args:
            page (playwright.sync_api.Page): page where component belongs to.
            locator (str): locator of the component.
            name (str): name of the component to display in Allure logs.
            input_type (str, optional): type of the field's input type
            ("input"/"textarea"). Defaults to "input".
            elements_selectors_override (dict, optional): dict of the
            component's elements sub-locators. Defaults to None (correspont
            to simple 'label', 'input'/'textarea' selectors).
        """

        super().__init__(page)

        self.name_prefix = name
        self.log(
            "Creating LinkAnnotatedField: "
            "locator=%s, input_type=%s, override=%s",
            locator,
            input_type,
            elements_selectors_override,
            level=DEBUG,
        )

        self.element_selectors = copy(self.selectors)
        if elements_selectors_override is not None:
            self.element_selectors.update(elements_selectors_override)
            self.log(
                "Elements selectors overriden: %s",
                self.element_selectors,
                level=DEBUG,
            )

        self.label = Label(
            page,
            f"{locator} {self.element_selectors['label']}",
            f"Label for {name}",
        )

        if input_type == "input":
            self.input = Input(
                page,
                f"{locator} {self.element_selectors['input']}",
                f"Input for {name}",
            )
        elif input_type == "textarea":
            self.input = Textarea(
                page,
                f"{locator} {self.element_selectors['textarea']}",
                f"Textarea for {name}",
            )

    @property
    def name(self):
        return f'"{self.name_prefix}" Field'

    # --- Actions
    def click_and_fill(
        self,
        value: str,
        mask_value: bool = False,
        validate_value: bool = False,
        **locator_qualifiers,
    ):
        """Clicks and then fills input with value"""
        self.log('Click and fill field input with "%s"', value)
        self.input.click_and_fill(
            value,
            mask_value=mask_value,
            validate_value=validate_value,
            **locator_qualifiers,
        )

    # --- Assertions
    def should_be_visible(
        self, label_only: bool = False, **locator_qualifiers
    ):
        """Checks that elements are visible. If 'label_only' flag is
        set to True - checks only Label element."""
        self.label.should_be_visible(**locator_qualifiers)
        if not label_only:
            self.input.should_be_visible(**locator_qualifiers)

    def should_have_label_text(self, text: str, **locator_qualifiers):
        """Checks that Label contains given test

        Args:
            text (str): text to find.
        """
        self.log('Check field\'s label text is "%s"', text)
        self.label.should_have_text(text, **locator_qualifiers)

    def should_have_value(self, value, mask_value=False, **locator_qualifiers):
        """Checks that input contains given value.

        Args:
            value (str): value to fill.
            mask_value (bool, optional): flag to mask value like '***ue' in
            reports. Defaults to False.
        """
        self.log(
            'Check field\'s input value is equal to "%s"',
            value if not mask_value else "**masked**",
        )
        self.input.should_have_value(
            value, mask_value=mask_value, **locator_qualifiers
        )
