"""Input elements class"""
import allure  # type: ignore
from playwright.sync_api import expect

from utils.helpers import mask_string_value

from .base_element import BaseElement


class Input(BaseElement):
    """Class for Input tag element"""

    @property
    def type_of(self) -> str:
        return "input"

    # --- Actions
    def click_and_fill(
        self,
        value: str | int | float,
        mask_value=False,
        validate_value=False,
        **locator_qualifiers,
    ):
        """Clicks and then fills input with value,
        Args:
            value (str): value to fill.
            mask_value (bool, optional): flag to mask value like '***ue' in
            reports. Defaults to False.
            validate_value (bool, optional): flag to validate value afterward.
            Defaults to False.
        """
        self.click(**locator_qualifiers)
        self.fill(
            value,
            mask_value=mask_value,
            validate_value=validate_value,
            **locator_qualifiers,
        )

    def fill(
        self,
        value: str | int | float,
        mask_value=False,
        validate_value=False,
        **locator_qualifiers,
    ):
        """Fills input with given value.

        Args:
            value (str): value to fill.
            mask_value (bool, optional): flag to mask value like '***ue' in
            reports. Defaults to False.
            validate_value (bool, optional): flag to validate value afterward.
            Defaults to False.
        """
        value_to_log = mask_string_value(str(value)) if mask_value else value
        with allure.step(
            f'Filling "{value_to_log}" into {self.type_of} with '
            f'name "{self.name}"'
        ):
            self.get_locator(**locator_qualifiers).fill(value=str(value))

            if validate_value:
                self.should_have_value(
                    str(value), mask_value=mask_value, **locator_qualifiers
                )

    # --- Assertions
    def should_have_value(self, value, mask_value=False, **locator_qualifiers):
        """Checks that input contains given value.

        Args:
            value (str): value to fill.
            mask_value (bool, optional): flag to mask value like '***ue' in
            reports. Defaults to False.
        """
        value_to_log = mask_string_value(value) if mask_value else value
        with allure.step(
            f"{self.type_of.capitalize()} with name "
            f'"{self.name}" should have value "{value_to_log}"'
        ):
            expect(self.get_locator(**locator_qualifiers)) \
                .to_have_value(value)
