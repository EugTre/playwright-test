"""Admin -> Geo Zones page"""
import allure
from playwright.sync_api import Page, expect
from utils.models.admin_geozone import GeozoneEntity, CountryZoneEntity
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

    def find_zone(self, zone: CountryZoneEntity, update_id: bool = False
                  ) -> tuple[int, int, str, str, str]:
        """Looks for zone in Zones table and selecting one with
        matching Country and Town values (or by zone_id if known)

        Args:
            zone (CountryZoneEntity): zone to find.
            update_id (bool, optional): flag to update given zone instance
            with found ID. Defaults to False.

        Raises:
            ValueError: on missing zone.

        Returns:
            tuple[int, int, str, str, str]: row_id, zone ID, country code,
            zone and city values from the row of found zone
        """
        table_values = self.get_added_zones_values()
        for row_idx, row_value in enumerate(table_values):
            zone_id, zone_name, zone_zone, zone_city, _ = row_value

            if any((
                zone.zone_id and zone.zone_id == zone_id,
                zone.value == zone_name and zone.city == zone_city
            )):
                if update_id:
                    zone.zone_id = zone_id

                return row_idx, int(zone_id), zone_name, zone_zone, zone_city

        raise ValueError(f"Failed to find Zone={zone} in table!")

    @allure.step("Deleting Geozone")
    def delete(self, confirm: bool = False):
        """Clicks 'Delete' button and optionally confirms in promt."""
        if confirm:
            self.page.on("dialog", lambda dialog: dialog.accept())

        self.delete_button.click()

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
        rows_data = self.get_added_zones_values()
        rows_content = list(zip(rows_text, rows_data))

        for expected_zone in geozone.zones:
            self.__validate_country_zone_entry(rows_content, expected_zone)

    @allure.step("Table data of {zone_entity} country "
                 "matches to expected")
    def __validate_country_zone_entry(self, rows_content, zone_entity):
        zone = zone_entity.value
        city = zone_entity.city

        for texts, values in rows_content:
            id_value, country_value, _, city_value = values

            if zone != country_value or city != city_value:
                continue

            id_text, country_text, _, city_text = texts
            with allure.step("Values are displayed"):
                assert id_text, \
                    '"ID" displayed value is empty ' \
                    f'for {zone} zone!'
                assert country_text, \
                    '"Country" displayed value is empty ' \
                    f'for {zone} zone!'
                assert city_text, \
                    f'"City" displayed value is empty for {zone} zone!'

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
        assert False, \
            f'Zone "{zone}" (city: {city}) is missing in the table! ' \
            f'Available items: \n{available_str}'
