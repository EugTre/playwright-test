"""Admin Login page"""
import allure
from playwright.sync_api import Page

from utils.elements import Input, Button, Banner
from utils.helpers import mask_string_value
from .base_page import BasePage
from .admin_main_page import AdminMainPage


class AdminLoginPage(BasePage):
    """Admin login page"""
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

        self.username_input = Input(
            page, "input[name=username]", "Username field"
        )
        self.password_input = Input(
            page, "input[name=password]", "Password field"
        )
        self.login_button = Button(
            page, "button[name=login]", "Login button"
        )
        self.failed_login_banner = Banner(
            page, ".alert-danger", "Failed login notification"
        )

    @property
    def url(self):
        return '/admin'

    def verify_page(self):
        self.login_button.should_be_visible()

    def login(self, username: str, password: str,
              expect_redirect=True,
              **locator_qualifiers) -> AdminMainPage:
        """Fills username and password, then presses login button.

        Args:
            username (str): username to fill.
            password (str): password to fill.
        """
        masked_password = mask_string_value(password)

        with allure.step(f'Logging as {username}/{masked_password}'):
            self.username_input.click(**locator_qualifiers)
            self.username_input.fill(username, **locator_qualifiers)

            self.password_input.click(**locator_qualifiers)
            self.password_input.fill(password, mask_value=True,
                                     **locator_qualifiers)

            self.login_button.click(**locator_qualifiers)

        return AdminMainPage(self.page, self.base_url) \
            if expect_redirect else None

    # --- Asserts
    @allure.step("Check login fail banner is displayed")
    def login_fail_banner_should_be_visible(self):
        """Checks that fail login attempt notification is displayed"""
        self.failed_login_banner.should_be_visible()

    @allure.step('Check text of the login failed banner to be equal "{text}"')
    def login_fail_banner_should_have_text(self, text: str):
        """Checks that fail login attempt notification have text"""
        self.login_fail_banner_should_be_visible()
        self.failed_login_banner.should_have_text(text)
