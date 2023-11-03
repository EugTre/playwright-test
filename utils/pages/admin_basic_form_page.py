"""Admin form page (unspecified)"""

import allure
from playwright.sync_api import Page

from utils.models.base_entity import BackOfficeEntity
from utils.components import AdminSideMenu, AdminTopMenu
from utils.elements import Title, Button

from .base_page import BasePage


class AdminBasicFormPage(BasePage):
    """Admin category page (basic).
    Supports only minumal number of common elements.
    Use specific category pages for advanced use."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.header_title = Title(
            page, "#main #content .card-title", "Form Title"
        )
        self.top_menu = AdminTopMenu(page)
        self.side_menu = AdminSideMenu(page)

        self.save_button = Button(
            page, "#content .card-action button[name='save']", "Save"
        )
        self.cancel_button = Button(
            page, "#content .card-action button[name='cancel']", "Cancel"
        )

    @property
    def url(self):
        """Return page's path URL."""
        return "/admin/?"

    @property
    def header(self) -> str:
        """Page header text"""
        return ""

    @property
    def breadcrumbs(self) -> tuple[str]:
        """Tuple of page's top menu breadcrumbs"""
        return tuple()

    def _verify_page_items(self):
        self.side_menu.should_be_visible()
        self.top_menu.should_be_visible()
        self.header_title.should_be_visible()

    # --- Actions
    @allure.step("Save form")
    def save(self) -> None:
        """Clicks save button at form"""
        self.log('Clicking "Save" button on form')
        self.save_button.click()

    @allure.step("Cancel form")
    def cancel(self):
        """Click Cancel button"""
        self.log("Exiting form by 'Cancel' button")
        self.cancel_button.click()

    def fill_from_entity(self, entity: BackOfficeEntity) -> None:
        """Fill form fields using given Geozone entity as
        a value"""

    # --- Assertions
    def header_text_should_match(self, header: str | None = None):
        """Verifies that header of the page match to given.

        If no 'header' text was given -- header from page descriptor
        will be used"""
        if header is None:
            header = self.header
        self.log('Checking page Header to be equal to "%s"', header)
        self.header_title.should_have_text(header)

    def breadcrumbs_should_match(self, items: tuple | list | None = None):
        """Verifies that breadcrumbs of the page match to given.

        If no 'items' were given -- items from page descriptor
        will be used"""
        if items is None:
            items = self.breadcrumbs
        self.top_menu.breadcrumbs_should_match(items)
