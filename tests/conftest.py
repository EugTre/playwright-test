"""Fixtures related to tests"""
import logging

import pytest
import allure
import utils.api_helpers as api

from utils import helpers
from utils.pages import (
    AdminLoginPage,
    AdminMainPage,
    AdminBasicCategoryPage
)
from utils.models.admin_geozone import (
    GeozoneEntity
)
from constants import (
    SUPERADMIN_USERNAME,
    SUPERADMIN_PASSWORD
)


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

    user = api.create_admin_user(session, base_url)
    logging.info('[Fixture] Created New Admin user for test: %s', user)

    return user


@allure.title("Create Geo Zone via API request")
@pytest.fixture
def new_geozone(request, base_url: str) -> GeozoneEntity:
    """Creates new geozone using API call and return
    geozone entity.

    Also handles geozone deletion after test finished."""

    options = request.node.get_closest_marker('new_geozone_options').kwargs
    countries = options.get('add_countries', None)
    geozone = helpers.generate_new_geozone_entity(countries)

    logging.info('[Fixture] Created Geozone for test: %s', geozone)

    session = api.prepare_logged_admin_session(
        base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )
    api.create_geo_zone(session, base_url, geozone)

    yield geozone
    logging.info('[Fixture] Removing Geozone created for test: %s', geozone)

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

    geozones = [gz for gz in geozones if gz is not None]

    if not geozones:
        return

    logging.info('[Fixture] Removing Geozones created for test: %s', geozones)
    session = api.prepare_logged_admin_session(
        base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )
    for gz_id in geozones:
        with allure.step(
            "Sending API request to delete Geo Zone "
            f"with id {gz_id}"
        ):
            api.delete_geo_zone(session, base_url, gz_id)
