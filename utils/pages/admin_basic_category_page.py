"""Admin category page (unspecified)"""

from playwright.sync_api import Page
from utils.elements import Title
from utils.components import AdminSideMenu, AdminTopMenu
from .admin_main_page import AdminMainPage


class AdminBasicCategoryPage(AdminMainPage):
    """Admin category page (basic).
    Supports only minumal number of common elements.
    Use specific category pages for advanced use."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.header_title = Title(
            page, "#main #content .card-title",
            "Title of the category"
        )

        self.top_menu = AdminTopMenu(page)
        self.side_menu = AdminSideMenu(page)

    @property
    def url(self):
        """Return page's path URL."""
        return '/admin'

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

    # --- Assertions
    def header_text_should_match(self, header: str | None = None):
        """Verifies that header of the page match to given.

        If no 'header' text was given -- header from page descriptor
        will be used"""
        if header is None:
            header = self.header
        self.header_title.should_have_text(header)

    def breadcrumbs_should_match(self, items: tuple | list | None = None):
        """Verifies that breadcrumbs of the page match to given.

        If no 'items' were given -- items from page descriptor
        will be used"""
        if items is None:
            items = self.breadcrumbs
        self.top_menu.breadcrumbs_should_match(items)
