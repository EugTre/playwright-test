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
from utils.models.admin_geozone import GeozoneEntity
from utils.pages import (
    AdminGeozonesPage,
    AdminGeozonesAddFormPage,
    AdminGeozonesEditFormPage
)
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

        with given("logged in admin user is at Geo Zones page"):
            pass

        with when("user clicks 'Create New Geo Zone' button"):
            form: AdminGeozonesAddFormPage = \
                admin_category_page.create_new_geozone()

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

        with given("logged in admin user is at Geo Zones page"):
            pass

        with when("user clicks 'Create New Geo Zone' button"):
            form: AdminGeozonesAddFormPage = \
                admin_category_page.create_new_geozone()

        with when("user fills 'Create New Geo Zone' form and "
                  "adding several countries"):
            geozone = helpers.generate_new_geozone_entity(
                add_countries=('MD', 'KZ', 'AM', 'VE')
            )
            form.fill_from_entity(geozone)

        with when("user saves form"):
            form.save()

        with then("user is redirected to GeoZones category page"):
            admin_category_page.verify_page()

        with then("created geo zone is in the list, have valid name "
                  "and number of zones"):
            _, entity_id, _, number_of_zones = \
                admin_category_page.find_geozone(geozone.name)
            handle_geozones.append(entity_id)

            assert number_of_zones == len(geozone.zones), \
                'Invalid number of Zones for newly created ' \
                f'Geozone "{geozone.name}"'

        with then("user sees success 'Changes saved' banner"):
            admin_category_page.banner_appeared_with_text(
                messages.get('Admin.Geozones OnCreateSuccess')
            )

    @allure.title("Existing Geo Zone may be viewed")
    @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    @pytest.mark.new_geozone_options(add_countries=('MD', 'KZ', 'AM', 'VE'))
    def test_view_created(self, admin_category_page: AdminGeozonesPage,
                          new_geozone: GeozoneEntity):
        """Verifies that created entity may be viewed via Edit form,
        and values are match to previously saved"""

        with given("logged admin user is at Geo Zones page"):
            admin_category_page.reload()

        with given("there is created Geozone entity in the table"):
            row_idx, geozone_id, geozone_name, zones_count = \
                admin_category_page.find_geozone(new_geozone.name)
            new_geozone.entity_id = geozone_id

            allure.attach(str(new_geozone), "Geozone Entity",
                          allure.attachment_type.TEXT)

            allure.attach(
                f"Row {row_idx}: ID={geozone_id}, Name={geozone_name}, "
                f"Zones={zones_count}",
                "Found Table Entry",
                allure.attachment_type.TEXT
            )

        with when("user clicks Edit button for entity"):
            edit_form: AdminGeozonesEditFormPage = \
                admin_category_page.edit_geozone(
                    row_id=row_idx,
                    entity_id=geozone_id
                )

        with then("user is navigated to Edit Geo Zone form"):
            edit_form.verify_page()
            edit_form.url_should_contain_entity_id()

        with then("form is populated with expected data"):
            edit_form.data_should_match_to(new_geozone)

        with then("added countries are ordered ascending with special rules"):
            names = edit_form.get_added_countries_names()
            sorted_names = helpers.order_by_rules(
                names,
                COUNTRIES_ORDERING_RULES
            )
            assert names == sorted_names, \
                "Countries in the dropdown are not A-Z ordered!"


    # @allure.title("Existing Geo Zone may be edited")
    # @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    # def test_edit(self, admin_category_page: AdminGeozonesPage,
    #                 created_geozone):
    #     with given("logged admin user is at Geo Zones page"):
    #         pass
    #     with given(f"there is Geozone entity in the table: {created_geozone}"):
    #         pass
    #     with when("user clicks Edit button for entity and navigated to Edit form"):
    #         pass
    #     with when("user is updates data in form and saves it"):
    #         pass
    #     with then("user is navigated to Geozone page"):
    #         pass
    #     with then("added countries zones are A-Z ordered"):
    #         pass
    #     with then("edited geo zone displayed with new name and number of zones"):
    #         entity_id, _, number_of_zones = \
    #             admin_category_page.get_geozone_info_by_name(geozone.name)

    #         geozone.entity_id = entity_id
    #         handle_geozones.append(entity_id)

    #         assert number_of_zones == len(geozone.zones), \
    #             'Invalid number of Zones for newly created ' \
    #             f'Geozone "{geozone.name}"'

    #     with then("user sees success 'Changes saved' banner"):
    #         admin_category_page.banner_appeared_with_text(
    #             messages.get('Admin.Geozones OnCreateSuccess')
    #         )

    #     with then("user can Edit zone again and see new values in Form"):
    #         admin_category_page.banner_appeared_with_text(
    #             messages.get('Admin.Geozones OnCreateSuccess')
    #         )

    # # TBD:
    # @allure.title("Existing Geo Zone may be deleted")
    # @pytest.mark.admin_category_page(AdminCategory.GEOZONES)
    # def test_delete(self, admin_category_page: AdminGeozonesPage,
    #                 created_geozone: str):
    #     """Tests it is possible to create new Geo Zone at
    #     Admin -> Geo Zones section"""

    #     with given("logged in admin user is at Geo Zones page"):
    #         pass

    #     with given("there is at least one Geo Zone exists"):
    #         pass

    #     with when("user clicks 'Edit' button for existing Geo Zone"):
    #         ...

    #     with when("user selects Delete and confirms deletion"):
    #         ...

    #     with then("user become redirected to Geo Zones pages and "
    #               "sees success 'Changes saved' banner"):
    #         ...

    #     with then("delete Geo Zone is not listed in table"):
    #         ...
