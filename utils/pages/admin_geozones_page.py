"""Admin -> Geo Zones page"""
import logging

import pytest
import allure

from playwright.sync_api import Page
from utils.elements import Button, Table, Banner
from utils.models.admin_geozone import GeozoneEntity
from .admin_basic_category_page import AdminBasicCategoryPage
from .admin_geozones_add_form_page import AdminGeozonesAddFormPage
from .admin_geozones_edit_form_page import AdminGeozonesEditFormPage


class AdminGeozonesPage(AdminBasicCategoryPage):
    """Admin -> Geo Zones page"""
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.create_new_button = Button(
            page, '#main #content .card-action a',
            "Create New Geo Zone"
        )

        self.notification_banner = Banner(
            page, ".alert-success", "Notification"
        )

        self.geozones_table = Table(
            page, "#content form table",
            "Geozones"
        )

        self.geozone_edit_button = Button(
            page, "#content form tbody tr:nth-child({row}) a.btn",
            "Edit"
        )

    @property
    def url(self):
        return "/admin/?app=geo_zones&doc=geo_zones"

    @property
    def header(self):
        return "Geo Zones"

    @property
    def breadcrumbs(self):
        return ('Geo Zones', )

    def _verify_page_items(self):
        super()._verify_page_items()
        self.header_title.should_have_text(self.header)

    # --- Actions
    def find_geozone(self, geozone: GeozoneEntity,
                     update_entity_id: bool = False
                     ) -> tuple[int, str, str, int]:
        """Returns geozone row index and data (id, name, zones counter)
        for row with given name in geozones table.

        Args (exclusive):
            geozone (GeozoneEntity): entity to find.
            update_entity_id (bool, optional). flag to update given entity
            with found data. Defaults to False.

        Returns:
            tuple in format
            (row_idx: int, entity_id: str, name: str, zones_count: int)"""
        if geozone.name is None and geozone.entity_id is None:
            raise ValueError(
                'Given geozone identifiers are missing '
                '(both "name" and "entity_id" are None)!'
            )

        target_name = geozone.name
        target_id = geozone.entity_id
        target_count = len(geozone.zones)
        logging.info("Looking for Geozones like: name=%s id=%s count=%s",
                     target_name, target_id, target_count)

        rows = self.geozones_table.get_rows_content()
        for row_idx, row in enumerate(rows):
            row_zone_id = row[1]
            row_zone_name = row[2]
            row_zone_count = int(row[3])

            logging.debug("Checking row %s: %s", row_idx, row)

            if all((
                not target_name or target_name == row_zone_name,
                not target_id or target_id == row_zone_id,
                target_count == row_zone_count
            )):
                allure.attach(
                    f"Row {row_idx}: ID={row_zone_id}, Name={row_zone_name}, "
                    f"Zones={row_zone_count}",
                    "Found Table Entry",
                    allure.attachment_type.TEXT
                )

                if update_entity_id:
                    geozone.entity_id = row_zone_id

                logging.info(
                    'Found GeoZone at row %s: id=%s name=%s count=%s',
                    row_idx, row_zone_id, row_zone_name, row_zone_count
                )

                return row_idx, row_zone_id, row_zone_name, row_zone_count

        rows_str = '\n'.join((f'  {str(row)}' for row in rows))
        raise ValueError(
            f'There is no row with Name={geozone.name}, '
            f'ID={geozone.entity_id} and Zones={target_count} '
            f'in the Geo Zones table!\nRows:\n{rows_str}'
        )

    def create_new_geozone(self) -> AdminGeozonesAddFormPage:
        """Clicks Create New Geozone button and
        returns Geozone Form page"""
        self.create_new_button.click()
        return AdminGeozonesAddFormPage(self.page)

    def edit_geozone(self,
                     geozone: GeozoneEntity,
                     row_id: str | None = None,
                     ) -> AdminGeozonesEditFormPage:
        """Clickes Edit button for selected geozone (by id or by name)"""
        if geozone is None and row_id is None:
            raise ValueError(
                "Geozone identifier is not given ('geozone' or 'row_id')!"
            )

        if row_id and geozone.entity_id:
            self.geozone_edit_button.click(row=row_id + 1)
            return AdminGeozonesEditFormPage(self.page, geozone.entity_id)

        row_id, found_entity_id, _, _ = self.find_geozone(geozone)

        # Shift +1 from 0-based index of py-array to 1-based of css selector
        self.geozone_edit_button.click(row=row_id + 1)
        return AdminGeozonesEditFormPage(self.page, found_entity_id)

    # --- Assertions
    @allure.step("Check geozone table is not empty")
    def geozones_should_not_be_empty(self):
        """Checks Geozone table to have at least 1
        row"""
        self.geozones_table.shold_not_be_empty()

    @allure.step("Check that notification banner "
                 "is displayed with text {text}")
    def banner_should_have_text(self, text: str):
        """Checks that notification banner is visible
        and have given text"""
        self.notification_banner.should_be_visible()
        self.notification_banner.should_have_text(text)

    @allure.step("Check that geozone metadata matches to expected")
    def geozone_metadata_should_match(self, geozone: GeozoneEntity):
        """Check that geozone metadata matches to expected"""
        _, entity_id, name, number_of_zones = self.find_geozone(geozone)

        with allure.step(f'Geozone name matches to "{geozone.name}"'):
            assert geozone.name == name, \
                'Name mismatches for ' \
                f'Geozone "{geozone.name}" (ID: {entity_id})'

        expected_count = len(geozone.zones)
        with allure.step(
            "Geozone number of zones matches (expected {expected_count})"
        ):
            assert expected_count == number_of_zones,  \
                'Number of zones mismatches for ' \
                f'Geozone "{geozone.name}" (ID: {entity_id})'

    @allure.step("Check that geozone is missing in the table")
    def geozone_should_be_missing(self, geozone: GeozoneEntity):
        """Checks that table is missing geozone entry with same
        id, name and zone count as given. Asserts otherwise.

        Args:
            geozone (GeozoneEntity): geozone to look for.
        """
        with pytest.raises(ValueError, match=r'There is no row with Name=.*'):
            self.find_geozone(geozone)
