"""Fixtures for tests"""
import random

import requests
import pytest

from utils.pages import AdminLoginPage, AdminMainPage
from constants import BASE_URL, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD


@pytest.fixture
def test_id(request):
    """Returns ID for parametrized test (like 'param1-param2-param3')."""
    return request.node.callspec.id


# --- Pages
@pytest.fixture
def admin_login_page(page) -> AdminLoginPage:
    """Returns Admin Login Page"""
    return AdminLoginPage(page, BASE_URL)


@pytest.fixture
def admin_main_page(page) -> AdminMainPage:
    """Returns Admin Main Page"""
    return AdminMainPage(page, BASE_URL)


# --- Data generation
@pytest.fixture
def new_admin_user(base_url: str) -> tuple[str, str]:
    """Creates new admin user"""
    # Generate username and password
    username = ''.join((
        'admin_',
        str(random.randrange(1000, 9999)),
        str(random.randrange(1000, 9999))
    ))
    password = '_'.join((
        random.choice(["salty", "sweet", "sour", "mild", "spicy", "juicy"]),
        random.choice(["cookie", "pie", "beef", "soup", "salad", "porridge"])
    ))

    # In case constants.BASE_URL is used instead of --base-url option
    # also remove tailing '/'
    if base_url == '':
        base_url = BASE_URL
    base_url = base_url.rstrip('/')

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Log in using super admin
    login_response = requests.post(
        f"{base_url}/admin/login.php",
        headers=headers,
        data='login=true&redirect_url=&login=Login'
             f'&username={SUPERADMIN_USERNAME}&password={SUPERADMIN_PASSWORD}',
        allow_redirects=False,
        timeout=10
    )
    # Re-use session cookie and make new request for user creation
    requests.post(
        f"{base_url}/admin/?app=users&doc=edit_user&page=1",
        headers=headers,
        cookies=login_response.cookies.copy(),
        data=f'username={username}&email='
             f'&password={password}&confirmed_password={password}'
             '&date_valid_from=2023-09-20T17%3A51'
             '&date_valid_to=2030-01-26T17%3A51&status=1&save=Save',
        timeout=10
    )

    return (username, password)
