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
    "utils.pages.countries.admin_countries_page",
    "utils.pages.countries.admin_countries_add_form_page",
    "utils.pages.geozones.admin_geozones_page",
    "utils.pages.geozones.admin_geozones_add_form_page",
    "utils.pages.geozones.admin_geozones_edit_form_page",
    "utils.pages.catalog.admin_catalog_page",
    "utils.pages.catalog.admin_catalog_add_form_page",
    "utils.pages.catalog.admin_catalog_edit_form_page",

    # Helper
    "utils.helpers"
)


def pytest_addoption(parser):
    """Add CLI options for pytest"""

    parser.addoption("--maximized",
                     action="store_true",
                     default=False,
                     help="Run tests in maximized mode.")

    parser.addoption("--skip-snapshot-check",
                     action="store_true",
                     default=False,
                     help="Optional flag to disable actual snapshot "
                     "verification (to save some time during debug)")
    parser.addoption("--snapshot-threshold",
                     action="store",
                     type=float,
                     default=0.3,
                     help="Snapshot comparison threshold in range 0...1.")

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

    config.addinivalue_line("markers",
                            "new_product_options(add_iamges): sets desired "
                            "options for 'new_product' fixture")

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

    pytest.pw_skip_snapshot_check = config.getoption("--skip-snapshot-check")
    pytest.pw_snapshot_threshold = config.getoption("--snapshot-threshold")

    if not config.option.base_url:
        config.option.base_url = BASE_URL

    pytest.pw_attach_console_errors_to_step = \
        config.getini("allure.console_errors_to_step")


@pytest.fixture
def prepared_page(page: Page, assert_snapshot) -> Page:
    """Prepares the page for tests:
    - add handling of browser console errors and optional
    attachement of browser errorr to allure steps;
    - maximize viewport if '--maximized' CLI option was set;
    """

    # --- Window size ---
    # Set window size if '--maximized' CLI option was used
    # Note: brwoser cli option to maximize works weird with PW,
    #       so this is a workaround
    if pytest.pw_window_size:
        page.set_viewport_size(pytest.pw_window_size)

    # --- Handle browser console errors ---
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

    # --- Snapshot comparison ---
    def assert_page_snapshot():
        if pytest.pw_skip_snapshot_check:
            logging.warning('Skipping snapshot comparison')
            return

        assert_snapshot(
            page.screenshot(),
            threshold=pytest.pw_snapshot_threshold
        )

    page.assert_snapshot = assert_page_snapshot

    yield page

    # --- Attaches browser errors to Allure report ---
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
