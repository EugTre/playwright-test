"""
epic('Admin')
feature('Categories')
story('Geo Zones')
"""
import allure  # type: ignore
import pytest

from constants import COUNTRIES_ORDERING_RULES
from utils import helpers
from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.admin_geozone import GeozoneEntity
from utils.pages import (
    AdminGeozonesEditFormPage,
    AdminGeozonesPage,
)

from .metadata import EPIC, FEATURE, STORY


@allure.title("Existing Geo Zone may be viewed")
@allure.epic(EPIC)
@allure.epic(FEATURE)
@allure.epic(STORY)
@pytest.mark.admin_category_page(AdminCategory.GEOZONES)
@pytest.mark.new_geozone_options(add_countries=("MD", "KZ", "AM", "VE"))
def test_view_created(
    admin_category_page: AdminGeozonesPage,
    new_geozone: GeozoneEntity,
):
    """Verifies that created entity may be viewed via Edit form,
    and values are match to previously saved"""
    with given("logged admin user is at Geo Zones page"):
        admin_category_page.reload()

    with given("there is created Geozone entity in the table"):
        row_idx = admin_category_page.find_in_table(
            new_geozone, True
        )

    with when("user clicks Edit button for entity"):
        edit_form: AdminGeozonesEditFormPage = (
            admin_category_page.edit_entry(
                row_idx=row_idx, entity=new_geozone
            )
        )

    with then("user is navigated to Edit Geo Zone form"):
        edit_form.verify_page()
        edit_form.url_should_contain_entity_id()

    with then("form is populated with expected data"):
        edit_form.form_data_should_match_to(new_geozone)

    with then("added countries are ordered ascending with special rules"):
        countries = edit_form.get_added_countries_names()
        helpers.compare_ordering(
            countries,
            COUNTRIES_ORDERING_RULES,
            "Countries in the dropdown are not A-Z ordered!",
        )
