"""Admin -> Geo Zones page"""
import allure

from playwright.sync_api import Page
from utils.elements import Button, Table, Banner
from .admin_basic_category_page import AdminBasicCategoryPage
from .admin_geozones_form_page import AdminGeozonesFormPage


class AdminGeozonesPage(AdminBasicCategoryPage):
    """Admin -> Geo Zones page"""
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.create_new_button = Button(
            page, '#main #content .card-action a',
            "Create New Zone button"
        )

        self.notification_banner = Banner(
            page, ".alert-success", "Notification banner"
        )

        self.geozones_table = Table(
            page, "#content form table",
            "Geozone table"
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

    def get_geozone_info_by_name(self, name: str) -> tuple[str, str, str]:
        """Returns geozone row data (id (str), name(str), number of zones(str))
        from row with given name in geozones table."""
        rows = self.geozones_table.get_rows_content()
        for row in rows:
            if row[2] == name:
                return row[1], row[2], int(row[3])

        raise ValueError(
            f"There is no row with 'Name' = {name} in the Geo Zones table!"
        )

    def click_create_new_geozone(self):
        """Clicks Create New Geozone button and
        returns Geozone Form page"""
        self.create_new_button.click()
        return AdminGeozonesFormPage(self.page)

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
