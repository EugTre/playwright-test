from typing import cast

import allure  # type: ignore

from constants import SUPERADMIN_PASSWORD, SUPERADMIN_USERNAME
from utils.bdd import given, then, when

from utils.pages import AdminLoginPage, AdminMainPage

from .metadata import EPIC, FEATURE, STORY


@allure.title("User can log in with valid credentials")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
def test_login(admin_login_page: AdminLoginPage):
    """User with valid creds can log in and main admin page is loaded"""
    with given("admin user with valid credentials is at login page"):
        username = SUPERADMIN_USERNAME
        password = SUPERADMIN_PASSWORD
        admin_login_page.visit()
        admin_login_page.verify_page()
        admin_login_page.should_match_snapshot()

    with when("user puts valid creds and presses Login button"):
        admin_page = admin_login_page.login(username, password)
        admin_page = cast(AdminMainPage, admin_page)

    with then("user become logged in and sees success notification"):
        admin_page.verify_page()
        admin_page.login_banner_shoule_be_visible()
