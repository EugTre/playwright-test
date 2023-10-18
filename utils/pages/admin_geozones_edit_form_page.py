"""Admin -> Geo Zones page"""
import allure
from playwright.sync_api import Page, expect
from utils.models.admin_geozone import GeozoneEntity
from utils.elements import Button
from .admin_geozones_add_form_page import AdminGeozonesAddFormPage


class AdminGeozonesEditFormPage(AdminGeozonesAddFormPage):
    """Admin -> Geo Zones page"""

    def __init__(self, page: Page, entity_id: str) -> None:
        super().__init__(page)
        self.entity_id = entity_id

        self.delete_button = Button(
            page, "#content .card-action button[name='delete']",
            "Delete"
        )

    @property
    def url(self):
        return "/admin/?app=geo_zones&doc=edit_geo_zone&page=1" \
            f"&geo_zone_id={self.entity_id}"

    @property
    def header(self):
        return " Edit Geo Zone"

    @property
    def breadcrumbs(self):
        return ('Geo Zones', 'Edit Geo Zone')

    def _verify_page_items(self):
        super()._verify_page_items()
        self.delete_button.should_be_visible()

    def get_added_countries_names(self):
        """Returns list of added countries from table"""
        return self.zone_table.get_rows_content(columns=(1,))

    # --- Assertions
    @allure.step("Check that page URL contains geo zone ID")
    def url_should_contain_entity_id(self):
        """Checks that pages url contains given entity_id"""
        expect(self.page).to_have_url(self.url)

    @allure.step("Check that form contain data that matches "
                 "to given geozone entity")
    def data_should_match_to(self, geozone: GeozoneEntity):
        """Checks that data in the fields is matching given
        geozone entity"""

        self.code_field.should_have_value(geozone.code)
        self.name_field.should_have_value(geozone.name)
        self.desc_field.should_have_value(geozone.description)

        if not geozone.zones:
            self.zone_table.shold_be_empty()
            return

        rows_text = self.zone_table.get_rows_content((0, 1, 2, 3))
        rows_data = self.zone_table.evaluate_on_nested_elements(
            nested_locator="input[type='hidden']",
            callback="nodes => Array.prototype.map.call(nodes, e => e.value)"
        )
        rows_content = list(zip(rows_text, rows_data))

        for expected_zone in geozone.zones:
            self.__validate_country_zone_entry(rows_content, expected_zone)

    @allure.step("Table data of {zone_entity} country "
                 "matches to expected")
    def __validate_country_zone_entry(self, rows_content, zone_entity):
        zone = zone_entity.value

        for texts, values in rows_content:
            if zone != values[1]:
                continue

            id_text, country_text, _, city_text = texts
            id_value, _, _, city_value = values

            with allure.step("Values match to expected"):
                assert zone_entity.city == city_value, \
                    '"City" value mismatch '\
                    f'for {zone} zone!'

            with allure.step("Values are displayed"):
                assert id_value, \
                    f'"ID" value is empty for {zone} zone!'
                assert id_text, \
                    '"ID" displayed value is empty ' \
                    f'for {zone} zone!'
                assert country_text, \
                    '"Country" displayed value is empty ' \
                    f'for {zone} zone!'

            with allure.step("Displayed values match to actual values"):
                assert id_value == id_text, \
                    'Value and displayed value mismatch for "ID" field ' \
                    f'for {zone} zone!'
                assert city_value == city_text, \
                    'Value and displayed value mismatch for "City" field ' \
                    f'for {zone} zone!'

            return

        # If not found - aseert
        available_str = '\n'.join([
            f'   {str(value)}' for _, value in rows_content
        ])
        assert False, f'Zone "{zone}" is missing in the table! ' \
            f'Zones available: \n{available_str}'
