"""
epic('Admin')
feature('Categories')
story('Geo Zones')
"""
import allure  # type: ignore
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.admin_geozone import GeozoneEntity
from utils.pages import (
    AdminGeozonesEditFormPage,
    AdminGeozonesPage,
)
from utils.text_repository import messages

from .metadata import EPIC, FEATURE, STORY


@allure.title("Existing Geo Zone may be deleted")
@allure.epic(EPIC)
@allure.epic(FEATURE)
@allure.epic(STORY)
@pytest.mark.admin_category_page(AdminCategory.GEOZONES)
@pytest.mark.new_geozone_options(add_countries=("KZ", "FR"))
def test_delete(
    admin_category_page: AdminGeozonesPage,
    new_geozone: GeozoneEntity,
):
    """Tests it is possible to create new Geo Zone at
    Admin -> Geo Zones section"""
    with given("logged in admin user is at Geo Zones page"):
        admin_category_page.reload()

    with given("there is created Geozone entity in the table"):
        row = admin_category_page.find_in_table(new_geozone, True)

    with when("user clicks 'Edit' button for existing Geo Zone"):
        edit_page: AdminGeozonesEditFormPage = (
            admin_category_page.edit_entry(new_geozone, row)
        )

    with when("user is navigated to Edit Geo Zone page"):
        edit_page.verify_page()

    with when("user selects Delete and confirms deletion"):
        edit_page.delete(confirm=True)

    with then("user is redirected to Geo Zones page"):
        admin_category_page.verify_page()

    with then("user sees success 'Changes saved' banner"):
        admin_category_page.banner_should_have_text(
            messages.get("General OnCreateSuccess")
        )

    with then("deleted Geo Zone is not listed in table"):
        admin_category_page.table_entry_should_be_missing(new_geozone)
