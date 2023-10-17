"""Admin -> Appearance -> Favicon page"""

from playwright.sync_api import Page
from utils.elements import Table
from .admin_basic_category_page import AdminBasicCategoryPage


class AdminCountriesPage(AdminBasicCategoryPage):
    """Admin -> Countries page"""
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.countries_table = Table(
            page, '#main #content table',
            'Countries table'
        )

    @property
    def url(self):
        return "/admin/?app=countries&doc=countries"

    @property
    def header(self):
        return "Countries"

    @property
    def breadcrumbs(self):
        return ('Countries', )

    def _verify_page_items(self):
        super()._verify_page_items()
        self.countries_table.should_be_visible()

    def get_countries(self) -> list:
        """Returns list of countries from table rows"""
        return [
            row[0]
            for row in self.countries_table.get_rows_content([4])
        ]

    def country_list_size_should_be(self, size: int):
        """Asserts size of the countries list"""
        self.countries_table.should_have_size_of(size)
