import allure  # type: ignore
import pytest

from utils.bdd import given, then, when

from utils.pages import AdminLoginPage
from utils.text_repository import messages

from .metadata import EPIC, FEATURE, STORY


@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.parametrize(
    "username, password, message",
    (
        ("", "", messages.get("Admin.Login ErrorOnEmptyUsername")),
        ("", "pass123", messages.get("Admin.Login ErrorOnEmptyUsername")),
        (
            "!@#$%^&*(()_+-=).,<>?'}",
            "",
            messages.get("Admin.Login ErrorOnNoUser"),
        ),
        (
            "my_user",
            "!@#$%^&*(()_+-=).,<>?'}",
            messages.get("Admin.Login ErrorOnNoUser"),
        ),
    ),
    ids=[
        "EmptyUser-EmptyPass",
        "EmptyUser-Pass",
        "UserNotExists-NoPass",
        "UserNotExists-Pass",
    ],
)
def test_login_fails(
    username,
    password,
    message,
    admin_login_page: AdminLoginPage,
    test_id: str,
):
    """User with invalid creds can not log in and see error message"""
    allure.dynamic.title(
        f"User can not log in with invalid credentials [{test_id}]"
    )

    with given(
        "admin user with invalid credentials "
        f'"{username}"/"{password}" is at login page'
    ):
        admin_login_page.visit()

    with when("user puts invalid creds and presses Login button"):
        admin_login_page.login(username, password, False)

    with then("user sees an error message"):
        admin_login_page.login_fail_banner_should_have_text(message)
