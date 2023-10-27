"""
epic('Admin')
feature('Categories')
story('Geo Zones')
"""
import allure
import pytest

from constants import COUNTRIES_ORDERING_RULES
from utils import helpers
from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.pages import (
    AdminGeozonesAddFormPage,
    AdminGeozonesPage,
)

from .metadata import EPIC, FEATURE, STORY


@allure.title("New Geo Zone form is available")
@allure.epic(EPIC)
@allure.epic(FEATURE)
@allure.epic(STORY)
@pytest.mark.admin_category_page(AdminCategory.GEOZONES)
def test_form_verification(admin_category_page: AdminGeozonesPage):
    """It is possible to access Create New Geo Zone from
    Admin -> Geo Zones page,
    all fields of the form are present;
    Country dropdown have all countries available;
    countries in Country dropdown are ordered
    (A-Z, with special rules applied)"""
    with given("logged in admin user is at Geo Zones page"):
        admin_category_page.reload()

    with when("user clicks 'Create New Geo Zone' button"):
        form: AdminGeozonesAddFormPage = (
            admin_category_page.create_new()
        )

    with then(
        "form 'Create New Geo Zone' is opened, "
        "contains expected fields and controls"
    ):
        form.verify_page()
        form.should_match_snapshot()

    with then("country list contains all countries"):
        form.country_options_size_should_be(243)

    with then("country list ordering is ascending with special rules"):
        options = form.get_country_option_names()
        helpers.compare_ordering(
            options,
            COUNTRIES_ORDERING_RULES,
            "Countries in the dropdown are not A-Z ordered!",
        )

    with then("clicking 'Cancel' returns user to Geo Zones page"):
        form.cancel()
        admin_category_page.verify_page()
