import allure  # type: ignore
import pytest

from constants import (
    COUNTRIES_ORDERING_RULES,
)
from utils import helpers
from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminCountriesPage

from .metadata import EPIC, FEATURE, STORY


@allure.title("List of countries is oredered (A-Z)")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.admin_category_page(AdminCategory.COUNTRIES)
def test_order(admin_category_page: AdminCountriesPage):
    """Tests that countries at Admin -> Countries section
    are listed in A-Z order except:
     - Åland Islands (must be treated as 'Aland Islands')
     - Türkiye (must be treated as 'Turkie')."""
    with given("logged in admin is at Countries category"):
        pass

    with when("list of countries is loaded"):
        admin_category_page.verify_page()
        admin_category_page.should_match_snapshot()

    with then("list of countries is not empty and contain 243 items"):
        admin_category_page.country_list_size_should_be(243)

    with then("countries ordering is ascending with special rules"):
        countries = admin_category_page.get_countries()
        helpers.compare_ordering(
            countries,
            COUNTRIES_ORDERING_RULES,
            "Countries in the table are not A-Z ordered!",
        )
