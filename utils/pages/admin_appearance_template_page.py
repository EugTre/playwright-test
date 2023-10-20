"""Admin -> Appearance -> Template page"""

from .admin_basic_category_page import AdminBasicCategoryPage


class AdminAppearanceTemplatePage(AdminBasicCategoryPage):
    """Admin -> Appearance -> Template page"""
    @property
    def url(self):
        return "/admin/?app=appearance&doc=template"

    @property
    def name(self):
        return "Admin/Appearance/Template"

    @property
    def header(self):
        return "Template"

    @property
    def breadcrumbs(self):
        return ('Appearance', 'Template')
