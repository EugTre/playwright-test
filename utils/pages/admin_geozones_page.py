"""Admin -> Geo Zones page"""
import allure

from playwright.sync_api import Page
from utils.elements import Button, Table, Banner
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

    def find_geozone(self, name: str = None, entity_id: str = None
                     ) -> tuple[int, str, str, int]:
        """Returns geozone row index and data (id, name, zones counter)
        for row with given name in geozones table.

        Args (exclusive):
            name (str, optional): name to search for. Defaults to None..
            entity_id (str, optional). ID to search for. Defaults to None.

        Returns:
            tuple in format
            (row_idx: int, entity_id: str, name: str, zones_count: int)"""
        if name is None and entity_id is None:
            raise ValueError(
                "Geozone identifier is not given ('name' or 'entity_id')!"
            )

        if entity_id is not None:
            target_value = entity_id
            target_column = 1
        else:
            target_value = name
            target_column = 2

        rows = self.geozones_table.get_rows_content()
        for row_idx, row in enumerate(rows):
            if row[target_column] == target_value:
                return row_idx, row[1], row[2], int(row[3])

        raise ValueError(
            f"There is no row with 'Name' = {name} in the Geo Zones table!"
        )

    def create_new_geozone(self) -> AdminGeozonesAddFormPage:
        """Clicks Create New Geozone button and
        returns Geozone Form page"""
        self.create_new_button.click()
        return AdminGeozonesAddFormPage(self.page)

    def edit_geozone(self,
                     name: str = None,
                     entity_id: str = None,
                     row_id: str | None = None,
                     ) -> AdminGeozonesEditFormPage:
        """Clickes Edit button for selected geozone (by id or by name)"""
        if name is None and entity_id is None and row_id is None:
            raise ValueError(
                "Geozone identifier is not given ('name' or 'entity_id')!"
            )

        if row_id and entity_id:
            self.geozone_edit_button.click(row=row_id + 1)
            return AdminGeozonesEditFormPage(self.page, entity_id)

        row_id, found_entity_id, _, _ = self.find_geozone(name)

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
    def banner_appeared_with_text(self, text: str):
        """Checks that notification banner is visible
        and have given text"""
        self.notification_banner.should_be_visible()
        self.notification_banner.should_have_text(text)
