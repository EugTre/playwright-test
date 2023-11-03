"""Button element class"""
import allure  # type: ignore

from .base_element import BaseElement


class Button(BaseElement):
    """Button element class, representing element of <button> tag"""

    @property
    def type_of(self) -> str:
        return "button"

    # --- Actions
    def hover(self, **locator_qualifiers) -> None:
        """Hovers mouse cursor over the button"""
        with allure.step(
            f"Hovering over {self.type_of} " f'with name "{self.name}"'
        ):
            self.get_locator(**locator_qualifiers).hover()

    def double_click(self, **locator_qualifiers) -> None:
        """Double clicks the button"""
        with allure.step(
            f"Double clicking {self.type_of} " f'with name "{self.name}"'
        ):
            self.get_locator(**locator_qualifiers).dblclick()
