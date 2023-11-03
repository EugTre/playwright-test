import allure  # type: ignore
import pytest

from utils.bdd import given, then, when

from utils.models.admin_user import UserEntity
from utils.pages import AdminLoginPage
from utils.text_repository import messages
from utils.steps import admin_users_steps

from .metadata import EPIC, FEATURE, STORY


@allure.title(
    "User have limited attempts to log in and use "
    "invalid creds {attempts_to_login} times"
)
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.parametrize(
    "attempts_to_login, message",
    (
        (1, messages.get("Admin.Login ErrorOnAttemptsLeft2")),
        (2, messages.get("Admin.Login ErrorOnAttemptsLeft1")),
        (3, messages.get("Admin.Login ErrorOnBlocked")),
    ),
    ids=("1 attempt", "2 attempts", "3 attempts"),
)
def test_login_failed_on_several_attempts(
    attempts_to_login,
    message,
    new_admin_user: UserEntity,
    admin_login_page: AdminLoginPage,
):
    """When using valid username user have limited number of
    attempts to log in"""
    # Log in as superuser and find user by id
    with given("valid admin user is created in the back office"):
        admin_users_steps.find_user_exists(
            admin_login_page, new_admin_user
        )

    with given(
        "admin user with valid username but invalid password "
        "is at login page"
    ):
        admin_login_page.visit()

    with when(f"user tries to login for {attempts_to_login} times"):
        for _ in range(attempts_to_login):
            admin_login_page.login(
                new_admin_user.username, "not-a-password", False
            )

    with then("user sees an error message"):
        admin_login_page.login_fail_banner_should_have_text(message)
