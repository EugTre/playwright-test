"""
epic('Admin')
feature('Categories')
story('Geo Zones')
"""
import allure
import pytest

from utils import helpers
from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.base_entity import BackOfficeEntity
from utils.pages import (
    AdminGeozonesAddFormPage,
    AdminGeozonesPage,
)
from utils.text_repository import messages

from .metadata import EPIC, FEATURE, STORY


@allure.title("New Geo Zone may be created")
@allure.epic(EPIC)
@allure.epic(FEATURE)
@allure.epic(STORY)
@pytest.mark.admin_category_page(AdminCategory.GEOZONES)
def test_create(
    admin_category_page: AdminGeozonesPage,
    handle_entities: list[BackOfficeEntity]
):
    """It's possible to create new Geo zone from Admin UI at
    Admin -> Geo Zones page;
    created zone is listed in table;
    created zone have valid name and number of zones added."""
    with given("logged in admin user is at Geo Zones page"):
        pass

    with when("user clicks 'Create New Geo Zone' button"):
        form: AdminGeozonesAddFormPage = (
            admin_category_page.create_new()
        )

    with when(
        "user fills 'Create New Geo Zone' form and "
        "adding several countries"
    ):
        geozone = helpers.generate_new_geozone_entity(
            add_countries=("MD", "KZ", "AM", "VE")
        )
        form.fill_from_entity(geozone)

    with when("user saves form"):
        form.save()

    with then("user is redirected to GeoZones category page"):
        admin_category_page.verify_page()

    with then(
        "created geo zone is in the list, have valid name "
        "and number of zones"
    ):
        admin_category_page.find_in_table(geozone, True)
        handle_entities.append(geozone)
        admin_category_page.table_entry_data_should_match(
            geozone
        )

    with then("user sees success 'Changes saved' banner"):
        admin_category_page.banner_should_have_text(
            messages.get("General OnCreateSuccess")
        )
