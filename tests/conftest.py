"""Fixtures related to tests"""
import logging

import allure
import pytest

import utils.api_helpers as api
from constants import SUPERADMIN_PASSWORD, SUPERADMIN_USERNAME
from utils.models.base_entity import BackOfficeEntity
from utils.models.entitiy_types import EntityType
from utils.models.admin_geozone import GeozoneEntity
from utils.models.admin_catalog import ProductEntity
from utils.pages import AdminBasicCategoryPage, AdminLoginPage, AdminMainPage


# --- Pages
# --- Helper functions
@allure.step("Login as Admin")
def login_as_admin_step(page):
    """Step to fullfill login form and log in"""
    login_page = AdminLoginPage(page)
    login_page.visit()
    return login_page.login(SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)


# --- Pages fixtures
@pytest.fixture
def admin_login_page(prepared_page) -> AdminLoginPage:
    """Returns Admin Login Page"""
    return AdminLoginPage(prepared_page)


@pytest.fixture
def admin_main_page(prepared_page) -> AdminMainPage:
    """Returns Admin Main Page"""
    admin_page = login_as_admin_step(prepared_page)
    return admin_page


@pytest.fixture
def admin_category_page(request, prepared_page) -> AdminBasicCategoryPage:
    """Returns Admin Category Page speciied by 'admin_category_page' marker
    of the test"""
    category = request.node.get_closest_marker("admin_category_page").args[0]
    admin_page = login_as_admin_step(prepared_page)
    category_page = admin_page.change_category(category)

    return category_page


# --- Data generation
@allure.step("Create new admin user via API request")
@pytest.fixture
def new_admin_user(base_url: str) -> tuple[str, str]:
    """Creates new admin user by API call"""
    # Generate username and password
    user = api.create_admin_user(
        base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )
    logging.info("[Fixture] Created New Admin user for test: %s", user)
    return user


@pytest.fixture
def new_geozone(request, base_url: str) -> GeozoneEntity:
    options = {
        "add_countries": None
    }
    marker = request.node.get_closest_marker("new_geozone_options")
    if marker and marker.kwargs:
        options.update(marker.kwargs)

    yield from api.get_new_entity(
        EntityType.GEOZONE, options, base_url,
        SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )


@pytest.fixture
def new_product(request, base_url: str) -> ProductEntity:
    options = {
        "images": None
    }

    marker = request.node.get_closest_marker("new_product_options")
    if marker and marker.kwargs:
        options.update(marker.kwargs)

    yield from api.get_new_entity(
        EntityType.PRODUCT, options, base_url,
        SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )


@pytest.fixture
def handle_entities(base_url: str):
    """Deletes object of HandledEntity protocol (e.g. GeozoneEntity,
    ProductEntity) after a test"""
    pool: list[BackOfficeEntity] = []
    yield pool

    entities = [
        entity
        for entity in pool
        if entity.entity_id
    ]

    if not entities:
        return

    logging.info(
        "[Fixture] Removing entities created during test: %s", entities
    )
    api.delete_entities(
        entities, base_url, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )
