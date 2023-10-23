"""Admin -> Appearance -> Favicon page"""

from .admin_basic_category_page import AdminBasicCategoryPage


class AdminAppearanceFaviconPage(AdminBasicCategoryPage):
    """Admin -> Appearance -> Favicon page"""

    @property
    def url(self):
        return "/admin/?app=appearance&doc=favicon"

    @property
    def name(self):
        return "Admin/Appearance/Favicon"

    @property
    def header(self):
        return "Favicon"

    @property
    def breadcrumbs(self):
        return ("Appearance", "Favicon")
