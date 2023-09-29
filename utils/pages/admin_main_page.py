"""Admin main page (after login)"""

from playwright.sync_api import Page
from utils.elements import Banner
from utils.components import AdminSideMenu, AdminTopMenu
from .base_page import BasePage


class AdminMainPage(BasePage):
    """Admin main page (after login)"""
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

        self.success_login_banner = Banner(
            page, ".alert-success", "Log In notification banner"
        )
        self.top_menu = AdminTopMenu(page)
        self.side_menu = AdminSideMenu(page)

    @property
    def url(self):
        return '/admin/'

    def verify_page(self):
        self.side_menu.should_be_visible()
        self.top_menu.should_be_visible()

    # --- Custom assertions
    def login_banner_shoule_be_visible(self):
        """Checks that login banner is visible"""
        self.success_login_banner.should_be_visible()
