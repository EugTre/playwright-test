"""Admin Page side menu"""
import allure

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
            page, "#sidebar > #box-apps-menu > .app[data-code={category}] > a",
            "Category button"
        )
        self.subcategory_button = Button(
            page, "#sidebar > #box-apps-menu .doc[data-id={category}] a",
            "Subcategory button"
        )

    @allure.step('Clicking category "{category}"')
    def click_category(self, category: str):
        """Clicks category button selected by given category enum"""
        self.category_button.click(category=category)

    @allure.step('Clicking sub-category "{category}"')
    def click_sub_category(self, category: str):
        """Clicks sub-category button selected by given category enum"""
        self.subcategory_button.click(category=category)

    def should_be_visible(self):
        self.logo_button.should_be_visible()
