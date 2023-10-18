"""Fixtures for tests"""
import tkinter

import pytest
from playwright.sync_api import Page
from constants import BASE_URL

# Allow assert representation
pytest.register_assert_rewrite(
    "utils.pages.admin_login_page",
    "utils.pages.admin_main_page",
    "utils.pages.admin_basic_category_page",
    "utils.pages.admin_appearance_template_page",
    "utils.pages.admin_appearance_favicon_page",
    "utils.pages.admin_catalog_page",
    "utils.pages.admin_countries_page",
    "utils.pages.admin_geozones_page",
    "utils.pages.admin_geozones_add_form_page",
    "utils.pages.admin_geozones_edit_form_page"
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
    config.addinivalue_line("markers",
                            "new_geozone_options(add_countries): sets desired "
                            "options for 'new_geozone' fixture")

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
