"""Admin Page side menu"""
from typing import TYPE_CHECKING

import allure  # type: ignore
from playwright.sync_api import Page

from utils.elements import Button

from .base_component import BaseComponent

if TYPE_CHECKING:
    from utils.models.admin_categories import AdminCategory


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
            page,
            "#sidebar > #box-apps-menu > .app[data-code={category}] > a",
            "Category button",
        )
        self.subcategory_button = Button(
            page,
            "#sidebar > #box-apps-menu .doc[data-id={category}] a",
            "Subcategory button",
        )

    @property
    def name(self):
        return "Side Menu"

    @allure.step("Switching category using side menu")
    def change_category(self, category: "AdminCategory"):
        """Performs series of cliks needed to change category page"""
        self.log("Swithing category in side menu to %s", category)

        category_id, subcategory_id, page_cls = category.value

        self.click_category(category_id)
        if subcategory_id is not None:
            self.click_sub_category(subcategory_id)

        new_page = page_cls(self.page)
        self.log("Category switched, new page is %s", new_page.name)

        return new_page

    @allure.step('Clicking category "{category}"')
    def click_category(self, category: str):
        """Clicks category button selected by given category enum"""
        self.category_button.click(category=category)

    @allure.step('Clicking sub-category "{category}"')
    def click_sub_category(self, category: str):
        """Clicks sub-category button selected by given category enum"""
        self.subcategory_button.click(category=category)

    def should_be_visible(self):
        self.log("Check that component is visible")
        self.logo_button.should_be_visible()
