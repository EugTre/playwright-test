"""Admin -> Appearance -> Favicon page"""

from .admin_basic_category_page import AdminBasicCategoryPage


class AdminCountriesPage(AdminBasicCategoryPage):
    """Admin -> Countries page"""
    @property
    def url(self):
        return "/admin/?app=countries&doc=countries"

    @property
    def header(self):
        return "Countries"

    @property
    def breadcrumbs(self):
        return ('Countries', )
