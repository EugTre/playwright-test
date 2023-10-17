"""
epic('Admin')
feature('Categories')
story('Geo Zones')
"""
import pytest
import allure

from utils import helpers
from utils.text_repository import messages
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminGeozonesPage, AdminGeozonesFormPage
from utils.bdd import given, when, then
from constants import COUNTRIES_ORDERING_RULES


@allure.epic('Admin')
@allure.feature('Categories')
@allure.story('Geo Zones')
class TestAdminCategoriesGeozones:
    """Tests related to Admin / Geo Zones category"""

    @allure.title("New Geo Zone form is available")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    def test_form_verification(self, admin_category_page: AdminGeozonesPage):
        """It is possible to access Create New Geo Zone from
        Admin -> Geo Zones page,
        all fields of the form are present;
        Country dropdown have all countries available;
        countries in Country dropdown are ordered
        (A-Z, with special rules applied)"""

        with given("logged in admin user is at Geo Zones category"):
            pass

        with when("user clicks 'Create New Geo Zone' button"):
            form: AdminGeozonesFormPage = \
                admin_category_page.click_create_new_geozone()

        with then("form 'Create New Geo Zone' is opened, "
                  "contains expected fields and controls"):
            form.verify_page()

        with then("country list contains all countries"):
            form.country_options_size_should_be(243)

        with then("country list ordering is ascending with special rules"):
            options = form.get_country_option_names()
            sorted_options = helpers.order_by_rules(
                options,
                COUNTRIES_ORDERING_RULES
            )

            assert options == sorted_options, \
                "Countries in the dropdown are not A-Z ordered!"

    @allure.title("New Geo Zone may be created")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    def test_create(self, admin_category_page: AdminGeozonesPage,
                    handle_geozones: list):
        """It's possible to create new Geo zone from Admin UI at
        Admin -> Geo Zones page;
        created zone is listed in table;
        created zone have valid name and number of zones added."""

        with given("logged in admin user is at Geo Zones category"):
            pass

        with when("user clicks 'Create New Geo Zone' button"):
            form: AdminGeozonesFormPage = \
                admin_category_page.click_create_new_geozone()

        with when("user fills 'Create New Geo Zone' form and "
                  "adding several countries in random order"):
            geozone = helpers.generate_new_geozone_entity(
                add_countries=('MD', 'KZ', 'AM', 'VE')
            )
            form.fill_from_entity(geozone)

        with when("user saves form"):
            form.save()

        with then("user is redirected to GeoZones category page"):
            admin_category_page.verify_page()

        with then("created geo zone is in list, have valid name "
                  "and number of zones"):
            entity_id, _, number_of_zones = \
                admin_category_page.get_geozone_info_by_name(geozone.name)

            geozone.entity_id = entity_id
            handle_geozones.append(geozone)

            assert number_of_zones == len(geozone.zones), \
                'Invalid number of Zones for newly created ' \
                f'Geozone "{geozone.name}"'

        with then("user sees success 'Changes saved' banner"):
            admin_category_page.banner_appeared_with_text(
                messages.get('Admin.Geozones OnCreateSuccess')
            )

    # TBD:
    @allure.title("Existing Geo Zone may be deleted")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    def test_delete(self, admin_category_page: AdminGeozonesPage,
                    created_geozone: str):
        """Tests it is possible to create new Geo Zone at
        Admin -> Geo Zones section"""

        with given("logged in admin user is at Geo Zones category"):
            pass

        with given("there is at least one Geo Zone exists"):
            pass

        with when("user clicks 'Edit' button for existing Geo Zone"):
            ...

        with when("user selects Delete and confirms deletion"):
            ...

        with then("user become redirected to Geo Zones pages and "
                  "sees success 'Changes saved' banner"):
            ...

        with then("delete Geo Zone is not listed in table"):
            ...
