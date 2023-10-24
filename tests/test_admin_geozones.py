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
from utils.models.base_entity import BackOfficeEntity
from utils.models.admin_geozone import CountryZoneEntity, GeozoneEntity
from utils.pages import (
    AdminGeozonesAddFormPage,
    AdminGeozonesEditFormPage,
    AdminGeozonesPage,
)
from utils.text_repository import messages


@allure.epic("Admin")
@allure.feature("Categories")
@allure.story("Geo Zones")
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

        with given("logged in admin user is at Geo Zones page"):
            pass

        with when("user clicks 'Create New Geo Zone' button"):
            form: AdminGeozonesAddFormPage = (
                admin_category_page.create_new()
            )

        with then(
            "form 'Create New Geo Zone' is opened, "
            "contains expected fields and controls"
        ):
            form.verify_page()

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

    @allure.title("New Geo Zone may be created")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    def test_create(
        self,
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

    @allure.title("Existing Geo Zone may be viewed")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    @pytest.mark.new_geozone_options(add_countries=("MD", "KZ", "AM", "VE"))
    def test_view_created(
        self,
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
            edit_form.data_should_match_to(new_geozone)

        with then("added countries are ordered ascending with special rules"):
            countries = edit_form.get_added_countries_names()
            helpers.compare_ordering(
                countries,
                COUNTRIES_ORDERING_RULES,
                "Countries in the dropdown are not A-Z ordered!",
            )

    @allure.title("Existing Geo Zone may be edited")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    @pytest.mark.new_geozone_options(add_countries=("US", "KZ", "BE", "FR"))
    def test_edit(
        self,
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
            edit_form.data_should_match_to(new_geozone)

    @allure.title("Existing Geo Zone may be deleted")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    @pytest.mark.new_geozone_options(add_countries=("KZ", "FR"))
    def test_delete(
        self,
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
            admin_category_page.geozone_should_be_missing(new_geozone)
