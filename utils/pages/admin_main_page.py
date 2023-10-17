"""Admin main page (after login)"""
from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page
from utils.elements import Banner
from utils.components import AdminSideMenu, AdminTopMenu
from .base_page import BasePage


if TYPE_CHECKING:
    from utils.models.admin_categories import AdminCategory


class AdminMainPage(BasePage):
    """Admin main page (after login)"""
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.notification_banner = Banner(
            page, ".alert-success", "Log In notification banner"
        )
        self.top_menu = AdminTopMenu(page)
        self.side_menu = AdminSideMenu(page)

    @property
    def url(self):
        return '/admin/'

    # -- Actions
    def _verify_page_items(self):
        self.side_menu.should_be_visible()
        self.top_menu.should_be_visible()

    def change_category(self, category: 'AdminCategory') -> BasePage:
        """Selects and clicks category item in side menu, and
        returns instance of basic category page (unspecified)"""
        category_id, subcategory_id, page_cls = category.value

        self.side_menu.click_category(category_id)
        if subcategory_id is not None:
            self.side_menu.click_sub_category(subcategory_id)

        return page_cls(self.page)

    # --- Custom assertions
    @allure.step("Check that notification banner is displayed "
                 "on successfull login")
    def login_banner_shoule_be_visible(self):
        """Checks that login banner is visible"""
        self.notification_banner.should_be_visible()
