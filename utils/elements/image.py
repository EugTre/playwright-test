"""Image element class"""
import allure  # type: ignore
from playwright.sync_api import expect

from utils.steps.admin_catalog_steps import step_compare_uploaded_images

from .base_element import BaseElement


class Image(BaseElement):
    """Represents <img> element"""

    @property
    def type_of(self) -> str:
        """Return name of the element's type."""
        return "image"

    def get_src_image(self, **locator_qualifiers) -> str | None:
        """Returns 'src' value of image element"""
        return self.get_locator(**locator_qualifiers).get_attribute("src")

    # --- Assertions
    def should_have_source(self, src: str, **locator_qualifiers) -> None:
        """Checks that element have given source."""
        locator = self.get_locator(**locator_qualifiers)
        self.log('Checking element to have source "%s" (%s)', src, locator)
        with allure.step(
            f"{self.type_of.capitalize()} with name "
            f'"{self.name}" should have source "{src}"'
        ):
            expect(locator).to_have_attribute("src", src)

    def source_should_match(self, match_to: str, **locator_qualifiers) -> None:
        """Checks that element have given source."""

        url = self.get_src_image(**locator_qualifiers)
        assert url, "Image's src is empty/not set!"

        response = self.page.context.request.get(url)

        step_compare_uploaded_images(
            original_image=match_to,
            uploaded_image=url,
            uploaded_image_content=response.body()
        )
