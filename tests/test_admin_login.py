"""
epic('Admin')
feature('Login')
story('Admin can log in')
"""

import pytest
import allure
from utils.pages import AdminLoginPage, AdminMainPage
from utils.bdd import given, when, then
from utils.text_repository import messages
from constants import SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD


@allure.epic('Admin')
@allure.feature('Login')
@allure.story('Admin can log in')
class TestAdminLogin:
    """Tests related to Admin log in story"""

    @allure.title("User can log in with valid credentials")
    def test_login(self, admin_login_page: AdminLoginPage):
        """User with valid creds can log in and main admin page is loaded"""
        with given("admin user with valid credentials is at login page"):
            username = SUPERADMIN_USERNAME
            password = SUPERADMIN_PASSWORD

            admin_login_page.visit()

        with when("user puts valid creds and presses Login button"):
            admin_page: AdminMainPage = admin_login_page.login(
                username, password
            )

        with then("user become logged in and sees success notification"):
            admin_page.verify_page()
            admin_page.login_banner_shoule_be_visible()

    # title("User can not log in with invalid credentials")
    @pytest.mark.parametrize("username, password, message", (
        (
            "", "",
            messages.get('Admin.Login ErrorOnEmptyUsername')
        ),
        (
            "", "pass123",
            messages.get('Admin.Login ErrorOnEmptyUsername')
        ),
        (
            "!@#$%^&*(()_+-=).,<>?'}", "",
            messages.get('Admin.Login ErrorOnNoUser')
        ),
        (
            "my_user", "!@#$%^&*(()_+-=).,<>?'}",
            messages.get('Admin.Login ErrorOnNoUser')
        )
    ), ids=[
            "EmptyUser-EmptyPass",
            "EmptyUser-Pass",
            "UserNotExists-NoPass",
            "UserNotExists-Pass"
        ]
    )
    def test_login_fails(self, username, password, message,
                         admin_login_page: AdminLoginPage,
                         test_id: str):
        """User with invalid creds can not log in and see error message"""
        allure.dynamic.title(
            f"User can not log in with invalid credentials [{test_id}]"
        )

        with given("admin user with invalid credentials "
                   f'"{username}"/"{password}" is at login page'):
            admin_login_page.visit()

        with when("user puts invalid creds and presses Login button"):
            admin_login_page.login(username, password, False)

        with then("user sees an error message"):
            admin_login_page.login_fail_banner_should_have_text(message)

    @allure.title("User have limited attempts to log in and use "
                  "invalid creds {attempts_to_login} times")
    @pytest.mark.parametrize("attempts_to_login, message", (
        (1, messages.get('Admin.Login ErrorOnAttemptsLeft2')),
        (2, messages.get('Admin.Login ErrorOnAttemptsLeft1')),
        (3, messages.get('Admin.Login ErrorOnBlocked')),
    ), ids=("1 attempt", "2 attempts", "3 attempts"))
    def test_login_failed_on_several_attempts(self, attempts_to_login, message,
                                              new_admin_user: tuple[str, str],
                                              admin_login_page: AdminLoginPage
                                              ):
        """When using valid username user have limited number of
        attempts to log in"""
        with given("admin user with valid username but invalid password "
                   "is at login page"):
            username, _ = new_admin_user
            admin_login_page.visit()

        with when(f"user tries to login for {attempts_to_login} times"):
            for _ in range(attempts_to_login):
                admin_login_page.login(username, "not-a-password", False)

        with then("user sees an error message"):
            admin_login_page.login_fail_banner_should_have_text(message)
