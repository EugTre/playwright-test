"""Fixtures for tests"""
import random
import tkinter

import requests
import pytest
from playwright.sync_api import Page

from utils.pages import AdminLoginPage, AdminMainPage
from constants import BASE_URL, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD


def pytest_addoption(parser):
    parser.addoption("--maximize",
                     action="store_true",
                     default=False,
                     help="Run tests in maximized mode.")


def pytest_configure(config):
    window_size = None
    if config.getoption("--maximize"):
        # Dirty way to get screen size to emulate
        # maximized browser
        tkapp = tkinter.Tk()
        width = tkapp.winfo_screenwidth()
        height = tkapp.winfo_screenheight()
        tkapp.destroy()

        window_size = {"width": width, "height": height}
    pytest.pw_window_size = window_size


@pytest.fixture
def maximizable_page(page) -> Page:
    """Wrapper for page to handle maximization in PW"""
    if pytest.pw_window_size:
        page.set_viewport_size(pytest.pw_window_size)
    return page


@pytest.fixture
def test_id(request):
    """Returns ID for parametrized test (like 'param1-param2-param3')."""
    return request.node.callspec.id


# --- Pages
@pytest.fixture
def admin_login_page(maximizable_page) -> AdminLoginPage:
    """Returns Admin Login Page"""
    return AdminLoginPage(maximizable_page, BASE_URL)


@pytest.fixture
def admin_main_page(maximizable_page) -> AdminMainPage:
    """Returns Admin Main Page"""
    return AdminMainPage(maximizable_page, BASE_URL)


# --- Data generation
@pytest.fixture
def new_admin_user(base_url: str) -> tuple[str, str]:
    """Creates new admin user by API call"""
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
    session = requests.session()
    session.headers.update(headers)

    # Log in using super admin and retrieve authorized session id cookie
    session.post(
        f"{base_url}/admin/login.php",
        data='login=true&redirect_url=&login=Login'
             f'&username={SUPERADMIN_USERNAME}&password={SUPERADMIN_PASSWORD}',
        allow_redirects=False,
        timeout=10
    )

    # Send API request to create new user
    session.post(
        f"{base_url}/admin/?app=users&doc=edit_user&page=1",
        data=f'username={username}&email='
             f'&password={password}&confirmed_password={password}'
             '&date_valid_from=2023-09-20T17%3A51'
             '&date_valid_to=2030-01-26T17%3A51&status=1&save=Save',
        timeout=10
    )

    return (username, password)
