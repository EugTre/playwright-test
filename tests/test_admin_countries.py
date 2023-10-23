"""
epic('Admin')
feature('Categories')
story('Countries')
"""
import allure
import pytest

from constants import (
    COUNTRIES_FIELDS_ANNOTATION_LINKS,
    COUNTRIES_ORDERING_RULES,
)
from utils import helpers
from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminCountriesAddFormPage, AdminCountriesPage


@allure.epic("Admin")
@allure.feature("Categories")
@allure.story("Countries")
@pytest.mark.admin_category_page(AdminCategory.COUNTRIES)
class TestAdminCategoriesCountries:
    """Tests related to Admin / Countries category"""

    @allure.title("List of countries is oredered (A-Z)")
    # @pytest.mark.admin_category_page(AdminCategory.COUNTRIES)
    def test_order(self, admin_category_page: AdminCountriesPage):
        """Tests that countries at Admin -> Countries section
        are listed in A-Z order except:
         - Åland Islands (must be treated as 'Aland Islands')
         - Türkiye (must be treated as 'Turkie')."""

        with given("logged in admin is at Countries category"):
            pass

        with when("list of countries is loaded"):
            admin_category_page.verify_page()

        with then("list of countries is not empty and contain 243 items"):
            admin_category_page.country_list_size_should_be(243)

        with then("countries ordering is ascending with special rules"):
            countries = admin_category_page.get_countries()
            helpers.compare_ordering(
                countries,
                COUNTRIES_ORDERING_RULES,
                "Countries in the table are not A-Z ordered!",
            )

    @allure.title("Create New Country form is available")
    # @pytest.mark.admin_category_page(AdminCategory.COUNTRIES)
    def test_form_verification(self, admin_category_page: AdminCountriesPage):
        """It is possible to access Create New Country from
        Admin -> Countries,
        - all fields and buttons of the form are present;
        - fields are anotated with external link to Wikipedia.org"""

        with given("logged in admin user is at Countries page"):
            pass

        with when("user clicks 'Create New Country' button"):
            form: AdminCountriesAddFormPage = admin_category_page.create_new()

        with then(
            "form 'Create New Country' is opened, "
            "contains expected fields and controls"
        ):
            form.verify_page()

        with then("form fields are annotated with link"):
            form.fields_should_be_annotated_with_links(
                COUNTRIES_FIELDS_ANNOTATION_LINKS
            )

        with then("annotation links opens in the new tab"):
            form.field_annotations_should_open_in_new_tabs()

        with then("clicking 'Cancel' returns user to Countries page"):
            form.cancel()
            admin_category_page.verify_page()
