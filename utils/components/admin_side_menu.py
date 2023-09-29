"""Admin Page side menu"""

from playwright.sync_api import Page
from utils.elements import Button
from .base_component import BaseComponent


class AdminSideMenu(BaseComponent):
    """Side menu at admin pages.
    Contains list of categories Logo and list of category buttons
    like Catalog, Customers, Settings, etc.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.logo_button = Button(
            page, "#sidebar > #logotype > a", "Logo button"
        )
        self.category_button = Button(
            page, "#sidebar > #box-apps-menu > li[data-code={category}] a",
            "Category button"
        )

    def should_be_visible(self):
        self.logo_button.should_be_visible()
