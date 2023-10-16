"""Admin -> Geo Zones page"""

from .admin_basic_category_page import AdminBasicCategoryPage


class AdminGeozonesPage(AdminBasicCategoryPage):
    """Admin -> Geo Zones page"""
    @property
    def url(self):
        return "/admin/?app=geo_zones&doc=geo_zones"

    @property
    def header(self):
        return "Geo Zones"

    @property
    def breadcrumbs(self):
        return ('Geo Zones', )
