"""Admin -> Catalog"""

from .admin_basic_category_page import AdminBasicCategoryPage


class AdminCatalogPage(AdminBasicCategoryPage):
    """Admin -> Catalog"""
    @property
    def url(self):
        return "/admin/?app=catalog&doc=catalog"

    @property
    def name(self):
        return "Admin/Catalog"

    @property
    def header(self):
        return "Catalog"

    @property
    def breadcrumbs(self):
        return ('Catalog', )
