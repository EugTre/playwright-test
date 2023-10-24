"""Admin -> Geo Zones page"""
# from logging import DEBUG

import allure
import pytest
from playwright.sync_api import Page

from utils.elements import Button, Label, Table
from utils.models.admin_geozone import GeozoneEntity
from utils.models.entry_lookup_strategy import (
    EntryLookupStrategy,
    EntryReadStrategy
)
from ..admin_basic_category_page import AdminBasicCategoryPage
from .admin_geozones_add_form_page import AdminGeozonesAddFormPage
from .admin_geozones_edit_form_page import AdminGeozonesEditFormPage


class AdminGeozonesPage(AdminBasicCategoryPage):
    """Admin -> Geo Zones page"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.table = Table(page, "#content form table", "Geo Zones")
        self.table.set_strategy(
            lookup=(
                EntryLookupStrategy(
                    column=1, field="id", selector='input', by_text=False,
                    is_primary_key=True
                ),
                EntryLookupStrategy(column=3, field="name"),
                EntryLookupStrategy(column=4, field="zones")
            ),
            texts=(
                EntryReadStrategy(column=3, selector="a"),
                EntryReadStrategy(column=4)
            )
        )

        self.create_new_button = Button(
            page, "#main #content .card-action a", "Create New Geo Zone"
        )

        self.notification_banner = Label(
            page, ".alert-success", "Notification banner"
        )

        self.geozone_edit_button = Button(
            page, "#content form tbody tr:nth-child({row}) a.btn", "Edit"
        )

    @property
    def url(self):
        return "/admin/?app=geo_zones&doc=geo_zones"

    @property
    def name(self):
        return "Admin/Geo Zones"

    @property
    def header(self):
        return "Geo Zones"

    @property
    def breadcrumbs(self):
        return ("Geo Zones",)

    def _verify_page_items(self):
        super()._verify_page_items()
        self.header_title.should_have_text(self.header)
        self.table.should_be_visible()

    # --- Actions
    def find_in_table(
        self, entity: GeozoneEntity, update_entity_id: bool = False
    ) -> int:
        """Returns geozone row index and data (id, name, zones counter)
        for row with given name in geozones table.

        Args (exclusive):
            entity (GeozoneEntity): entity to find.
            update_entity_id (bool, optional). flag to update given entity
            with found data. Defaults to False.

        Returns:
            tuple in format
            (row_idx: int, entity_id: str, name: str, zones_count: int)"""
        self.log(
            "Looking for Geozones like: %s",
            entity.get_lookup_params()
        )

        row_idx = self.table.find_entry(entity)
        self.log("Found at row %s", row_idx)

        if update_entity_id:
            entity.entity_id = self.table.get_entry_texts(
                row_idx, [EntryReadStrategy(column=2)]
            )[0]

        allure.attach(
            f"At Row {row_idx}. Entity: {entity}",
            "Entry Found", allure.attachment_type.TEXT
        )

        return row_idx

    def create_new(self) -> AdminGeozonesAddFormPage:
        """Clicks Create New Geozone button and
        returns Geozone Form page"""
        self.create_new_button.click()
        return AdminGeozonesAddFormPage(self.page)

    def edit_entry(
        self,
        entity: GeozoneEntity,
        row_idx: str | None = None,
    ) -> AdminGeozonesEditFormPage:
        """Clickes Edit button for selected geozone (by id or by name)"""
        if entity is None and row_idx is None:
            raise ValueError(
                "Geozone identifier is not given ('geozone' or 'row_id')!"
            )

        if row_idx and entity.entity_id:
            self.geozone_edit_button.click(row=row_idx + 1)
            return AdminGeozonesEditFormPage(self.page, entity.entity_id)

        row_idx = self.find_in_table(entity, True)

        # Shift +1 from 0-based index of py-array to 1-based of css selector
        self.geozone_edit_button.click(row=row_idx + 1)
        return AdminGeozonesEditFormPage(self.page, entity.entity_id)

    # --- Assertions
    @allure.step(
        "Check that notification banner is displayed with text {text}"
    )
    def banner_should_have_text(self, text: str):
        """Checks that notification banner is visible
        and have given text"""
        self.notification_banner.should_be_visible()
        self.notification_banner.should_have_text(text)

    @allure.step("Check that geozone metadata matches to expected")
    def table_entry_data_should_match(self, entity: GeozoneEntity):
        """Check that geozone metadata matches to expected"""

        self.log("Checking table entry to match %s", entity)
        with allure.step("Entry is in table"):
            row_idx = self.find_in_table(entity)
            self.table.entry_should_be_visible(row_idx)

        data_name, data_zones_count = \
            self.table.get_entry_texts(row_idx)

        with allure.step(f'Geozone name matches to "{entity.name}"'):
            assert entity.name == data_name, \
                'Name mismatches for ' \
                f'Geozone "{entity.name}" (ID: {entity.entity_id})'

        expected_count = len(entity.zones)
        with allure.step(
            f"Geozone number of zones matches (expected {expected_count})"
        ):
            assert expected_count == int(data_zones_count),  \
                'Number of zones mismatches for ' \
                f'Geozone "{entity.name}" (ID: {entity.entity_id})'

    @allure.step("Check that geozone is missing in the table")
    def geozone_should_be_missing(self, entity: GeozoneEntity):
        """Checks that table is missing geozone entry with same
        id, name and zone count as given. Asserts otherwise.

        Args:
            entity (GeozoneEntity): geozone to look for.
        """
        with pytest.raises(
            ValueError, match=r"There is no row with data like.*"
        ):
            self.find_in_table(entity)
