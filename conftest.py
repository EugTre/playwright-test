"""Fixtures for tests"""
import logging
import tkinter

import allure
import pytest
from playwright.sync_api import Page

from constants import BASE_URL

# Allow assert representation
pytest.register_assert_rewrite(
    # Pages
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

    # Helper
    "utils.helpers"
)


def pytest_addoption(parser):
    """Add CLI options for pytest"""
    parser.addoption("--maximized",
                     action="store_true",
                     default=False,
                     help="Run tests in maximized mode.")
    parser.addini("allure.console_errors_to_step",
                  "Attach browser console error to Allure step",
                  type='bool',
                  default=True)


def pytest_configure(config):
    """Configure pytest before tests execution"""
    config.addinivalue_line("markers",
                            "admin_category_page(name): sets name of category "
                            "page to retrieve")
    config.addinivalue_line("markers",
                            "new_geozone_options(add_countries): sets desired "
                            "options for 'new_geozone' fixture")

    window_size = None
    if config.getoption("--maximized"):
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

    pytest.pw_attach_console_errors_to_step = \
        config.getini("allure.console_errors_to_step")


@pytest.fixture
def prepared_page(page: Page) -> Page:
    """Prepares the page for tests:
    - add handling of browser console errors and optional
    attachement of browser errorr to allure steps;
    - maximize viewport if '--maximized' CLI option was set;
    """

    # Set window size if '--maximized' CLI option was used
    if pytest.pw_window_size:
        page.set_viewport_size(pytest.pw_window_size)

    # Handle browser console errors
    browser_errors = []

    def log_console_error_msg(msg):
        """Logs browser console error to log"""
        if msg.type != 'error':
            return

        reported_error = f"Page: {msg.page}; text: {msg.text}."
        logging.warning(
            "Browser Console error! %s",
            reported_error
        )
        browser_errors.append(reported_error)
        if pytest.pw_attach_console_errors_to_step:
            allure.attach(
                reported_error,
                "Browser Error",
                allure.attachment_type.TEXT
            )

    page.on("console", log_console_error_msg)

    yield page

    if not browser_errors:
        return

    allure.attach(
        '\n'.join(browser_errors),
        "Browser Errors (All)",
        allure.attachment_type.TEXT
    )
    logging.warning(
        "There were %s browser console error(s) occured during the test.",
        len(browser_errors)
    )


@pytest.fixture
def test_id(request):
    """Returns ID for parametrized test (like 'param1-param2-param3')."""
    return request.node.callspec.id
