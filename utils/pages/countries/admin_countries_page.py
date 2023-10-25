"""Admin -> Appearance -> Favicon page"""
from logging import DEBUG

import allure
from playwright.sync_api import Page

from utils.elements import Button

from ..admin_basic_category_page import AdminBasicCategoryPage
from .admin_countries_add_form_page import AdminCountriesAddFormPage


class AdminCountriesPage(AdminBasicCategoryPage):
    """Admin -> Countries page"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.create_new_button = Button(
            page, "#main #content .card-action a", "Create New Country"
        )

    @property
    def url(self):
        return "/admin/?app=countries&doc=countries"

    @property
    def name(self):
        return "Admin/Countries"

    @property
    def header(self):
        return "Countries"

    @property
    def breadcrumbs(self):
        return ("Countries",)

    def _verify_page_items(self):
        super()._verify_page_items()
        self.table.should_be_visible()

    def get_countries(self) -> list:
        """Returns list of countries from table rows"""
        countries_names = [
            row[0] for row in self.table.get_rows_content([4])
        ]

        self.log("Countries table has %s items", len(countries_names))
        self.log(
            "List of countries in table: %s", countries_names, level=DEBUG
        )

        return countries_names

    # --- Actions
    def create_new(self) -> AdminCountriesAddFormPage:
        """Clicks 'Create New Country' button and returns
        form page"""
        self.log("Clicking 'Create New Country' button")
        self.create_new_button.click()
        return AdminCountriesAddFormPage(self.page)

    # --- Assertions
    @allure.step("Check that list of countries have {size} element(s)")
    def country_list_size_should_be(self, size: int):
        """Asserts size of the countries list"""
        self.log("Checking size of the 'Countries' table to be %s", size)
        self.table.should_have_size_of(size)
