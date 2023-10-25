"""Module with collection of classes that represent pages"""
# flake8: noqa

from .admin_basic_category_page import AdminBasicCategoryPage
from .admin_basic_form_page import AdminBasicFormPage

from .admin_appearance_favicon_page import AdminAppearanceFaviconPage
from .admin_appearance_template_page import AdminAppearanceTemplatePage
from .admin_login_page import AdminLoginPage
from .admin_main_page import AdminMainPage

from .catalog.admin_catalog_page import AdminCatalogPage
from .catalog.admin_catalog_add_form_page import AdminCatalogAddFormPage
from .catalog.admin_catalog_edit_form_page import AdminCatalogEditFormPage

from .countries.admin_countries_add_form_page import AdminCountriesAddFormPage
from .countries.admin_countries_page import AdminCountriesPage

from .geozones.admin_geozones_add_form_page import AdminGeozonesAddFormPage
from .geozones.admin_geozones_edit_form_page import AdminGeozonesEditFormPage
from .geozones.admin_geozones_page import AdminGeozonesPage

from .users.admin_users_page import AdminUsersPage
