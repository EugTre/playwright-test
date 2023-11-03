"""
epic('Admin')
feature('Categories')
story('Geo Zones')
"""
import allure  # type: ignore
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.admin_geozone import CountryZoneEntity, GeozoneEntity
from utils.pages import (
    AdminGeozonesEditFormPage,
    AdminGeozonesPage,
)
from utils.text_repository import messages

from .metadata import EPIC, FEATURE, STORY


@allure.title("Existing Geo Zone may be edited")
@allure.epic(EPIC)
@allure.epic(FEATURE)
@allure.epic(STORY)
@pytest.mark.admin_category_page(AdminCategory.GEOZONES)
@pytest.mark.new_geozone_options(add_countries=("US", "KZ", "BE", "FR"))
def test_edit(
    admin_category_page: AdminGeozonesPage,
    new_geozone: GeozoneEntity,
):
    """Tests that existing geozone may be updated through UI:
    - change CODE, NAME and DESCRIPTION
    - remove ZONE added zone
    - add new ZONE"""
    with given("logged admin user is at Geo Zones page"):
        admin_category_page.reload()

    with given("there is created Geozone entity in the table"):
        row = admin_category_page.find_in_table(new_geozone, True)

    with when("user clicks Edit button for entity and opens Edit form"):
        edit_form: AdminGeozonesEditFormPage = (
            admin_category_page.edit_entry(new_geozone, row_idx=row)
        )
        edit_form.verify_page()

    with when("user is updates data in form and saves it"):
        # Change zone data, and re-populate form
        new_geozone.code = "XTEST"
        new_geozone.description = "New Description"
        new_geozone.name = "XXX-edited-zone-name"
        new_geozone.zones = [
            CountryZoneEntity(value="AM", city="TownA"),
            CountryZoneEntity(value="AM", city="TownB"),
        ]

        edit_form.remove_zones()
        edit_form.fill_from_entity(new_geozone)
        edit_form.save()

    with then("user is navigated to Geozone page"):
        admin_category_page.verify_page()

    with then("edited name and number of zones is displayed for zone"):
        admin_category_page.table_entry_data_should_match(new_geozone)

    with then("user sees success 'Changes saved' banner"):
        admin_category_page.banner_should_have_text(
            messages.get("General OnCreateSuccess")
        )

    with then("user can Edit zone again and see new values in Form"):
        edit_form = admin_category_page.edit_entry(new_geozone)
        edit_form.form_data_should_match_to(new_geozone)
