"""Admin Login page"""
import allure
from playwright.sync_api import Page

from utils.elements import Button, Input, Label
from utils.helpers import mask_string_value

from .admin_main_page import AdminMainPage
from .base_page import BasePage


class AdminLoginPage(BasePage):
    """Admin login page"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username_input = Input(
            page, "input[name=username]", "Username field"
        )
        self.password_input = Input(
            page, "input[name=password]", "Password field"
        )
        self.login_button = Button(page, "button[name=login]", "Login button")
        self.failed_login_banner = Label(
            page, ".alert-danger", "Failed login notification"
        )

    @property
    def url(self):
        return "/admin"

    @property
    def name(self):
        return "Admin/Login"

    def _verify_page_items(self):
        self.login_button.should_be_visible()

    def login(
        self,
        username: str,
        password: str,
        expect_redirect=True,
    ) -> AdminMainPage:
        """Fills username and password, then presses login button.

        Args:
            username (str): username to fill.
            password (str): password to fill.
        """
        masked_password = mask_string_value(password)
        self.log("Logging in using creds %s/%s", username, masked_password)

        with allure.step(f"Logging as {username}/{masked_password}"):
            self.username_input.click()
            self.username_input.fill(username)

            self.password_input.click()
            self.password_input.fill(password, mask_value=True)

            self.login_button.click()

        return AdminMainPage(self.page) if expect_redirect else None

    # --- Asserts
    @allure.step("Check login fail banner is displayed")
    def login_fail_banner_should_be_visible(self):
        """Checks that fail login attempt notification is displayed"""
        self.log("Check that notification banner is visible")
        self.failed_login_banner.should_be_visible()

    @allure.step('Check text of the login failed banner to be equal "{text}"')
    def login_fail_banner_should_have_text(self, text: str):
        """Checks that fail login attempt notification have text"""
        self.login_fail_banner_should_be_visible()

        self.log('Check that notification banner text is "%s"', text)
        self.failed_login_banner.should_have_text(text)
