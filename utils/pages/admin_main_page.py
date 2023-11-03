"""Admin main page (after login)"""
import allure
from playwright.sync_api import Page

from utils.components import AdminSideMenu, AdminTopMenu
from utils.elements import Label

from .base_page import BasePage


class AdminMainPage(BasePage):
    """Admin main page (after login)"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.notification_banner = Label(
            page, ".alert-success", "Log In notification banner"
        )
        self.top_menu = AdminTopMenu(page)
        self.side_menu = AdminSideMenu(page)

    @property
    def url(self):
        return "/admin/"

    @property
    def name(self):
        return "Admin/Dashboard"

    # -- Actions
    def _verify_page_items(self):
        self.side_menu.should_be_visible()
        self.top_menu.should_be_visible()

    # --- Custom assertions
    @allure.step(
        "Check that notification banner is displayed " "on successfull login"
    )
    def login_banner_shoule_be_visible(self):
        """Checks that login banner is visible"""
        self.notification_banner.should_be_visible()
