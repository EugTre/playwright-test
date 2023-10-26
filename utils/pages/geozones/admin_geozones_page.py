"""Admin -> Geo Zones page"""
# from logging import DEBUG

import allure
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

    @property
    def table_row_lookup_strategy(self) -> tuple[EntryLookupStrategy]:
        return (
            EntryLookupStrategy(
                column=1, field="id", selector='input', by_text=False,
                is_primary_key=True
            ),
            EntryLookupStrategy(column=3, field="name"),
            EntryLookupStrategy(column=4, field="zones")
        )

    @property
    def table_get_row_text_strategy(self) -> tuple[EntryReadStrategy]:
        return (
            EntryReadStrategy(column=2),
            EntryReadStrategy(column=3, selector="a"),
            EntryReadStrategy(column=4)
        )

    def _verify_page_items(self):
        super()._verify_page_items()
        self.header_title.should_have_text(self.header)
        self.table.should_be_visible()

    # --- Actions
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

        if not row_idx or not entity.entity_id:
            row_idx = self.find_in_table(entity, True)

        # Note:
        # Shift row_idx +1 from 0-based index of py-array
        # to 1-based of css selector
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
        data_id, data_name, data_zones_count = \
            self.get_row_text_for_entity(entity)

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

        with allure.step(
            f"Displayed ID match to actual ID {entity.entity_id}"
        ):
            assert entity.entity_id == data_id, \
                'Geozone displayed ID mismatches for ' \
                f'Geozone "{entity.name}" (ID: {entity.entity_id})'
