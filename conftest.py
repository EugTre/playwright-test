"""Fixtures for tests"""
import tkinter

import pytest
import allure
from playwright.sync_api import Page

import utils.api_helpers as api
from utils import helpers
from utils.models.admin_geozone import GeozoneEntity
from utils.pages import AdminLoginPage, AdminMainPage, AdminBasicCategoryPage
from constants import (
    BASE_URL,
    SUPERADMIN_USERNAME,
    SUPERADMIN_PASSWORD
)


def pytest_addoption(parser):
    """Add CLI options for pytest"""
    parser.addoption("--maximize",
                     action="store_true",
                     default=False,
                     help="Run tests in maximized mode.")


def pytest_configure(config):
    """Configure pytest before tests execution"""
    config.addinivalue_line("markers",
                            "admin_category_page(name): sets name of category "
                            "page to retrieve")

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

    if not config.option.base_url:
        config.option.base_url = BASE_URL


@pytest.fixture(name='maximizable_page')
def maximize_page_viewport(page) -> Page:
    """Wrapper for page to handle maximization in PW"""
    if pytest.pw_window_size:
        page.set_viewport_size(pytest.pw_window_size)
    return page


@pytest.fixture
def test_id(request):
    """Returns ID for parametrized test (like 'param1-param2-param3')."""
    return request.node.callspec.id


# --- Pages
# --- Helper functions
@allure.step("Login as Admin")
def login_as_admin_step(page):
    """Step to fullfill login form and log in"""
    login_page = AdminLoginPage(page)
    login_page.visit()
    return login_page.login(
        SUPERADMIN_USERNAME,
        SUPERADMIN_PASSWORD
    )


# --- Pages fixtures
@pytest.fixture
def admin_login_page(maximizable_page) -> AdminLoginPage:
    """Returns Admin Login Page"""
    return AdminLoginPage(maximizable_page)


@pytest.fixture
def admin_main_page(maximizable_page) -> AdminMainPage:
    """Returns Admin Main Page"""
    admin_page = login_as_admin_step(maximizable_page)
    return admin_page


@pytest.fixture
def admin_category_page(request, maximizable_page) -> AdminBasicCategoryPage:
    """Returns Admin Category Page speciied by 'admin_category_page' marker
    of the test"""
    category = request.node.get_closest_marker('admin_category_page').args[0]
    admin_page = login_as_admin_step(maximizable_page)
    category_page = admin_page.change_category(category)

    return category_page


# --- Data generation
@allure.title("Create new admin user via API request")
@pytest.fixture
def new_admin_user(base_url: str) -> tuple[str, str]:
    """Creates new admin user by API call"""
    # Generate username and password
    session = api.prepare_logged_admin_session(
        base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )

    return api.create_admin_user(session, base_url)


@allure.title("Create Geo Zone via API request")
@pytest.fixture
def new_geozone(base_url: str) -> GeozoneEntity:
    """Creates new geozone using API call and return
    geozone entity.

    Also handles geozone deletion after test finished."""

    geozone = helpers.generate_new_geozone_entity()
    session = api.prepare_logged_admin_session(
        base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )

    api.create_empty_geo_zone(session, base_url, geozone)

    yield geozone

    with allure.step("Sending API request to delete Geo Zone "
                     f"with id {geozone.entity_id}"):
        api.delete_geo_zone(session, base_url, geozone.entity_id)


@pytest.fixture
def handle_geozones(base_url: str):
    """Allows to handle geozone entities deletion
    after test finished.
    """
    geozones = []
    yield geozones

    geozones = [gz.entity_id
                for gz in geozones
                if gz.entity_id is not None]

    if not geozones:
        return

    session = api.prepare_logged_admin_session(
        base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )
    for gz_id in geozones:
        with allure.step(
            "Sending API request to delete Geo Zone "
            f"with id {gz_id}"
        ):
            api.delete_geo_zone(session, base_url, gz_id)
