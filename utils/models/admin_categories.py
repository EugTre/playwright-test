"""Useful data representation classes"""
from enum import Enum

from utils.pages import (
    AdminAppearanceFaviconPage,
    AdminAppearanceTemplatePage,
    AdminCatalogPage,
    AdminCountriesPage,
    AdminGeozonesPage,
    AdminUsersPage
)


class AdminCategory(Enum):
    """Categories for Admin Side menu"""

    APPEARANCE = ("appearance", None, AdminAppearanceTemplatePage)
    APPEARANCE_TEMPLATE = (
        "appearance",
        "template",
        AdminAppearanceTemplatePage,
    )
    APPEARANCE_FAVICON = ("appearance", "favicon", AdminAppearanceFaviconPage)
    CATALOG = ("catalog", None, AdminCatalogPage)
    COUNTRIES = ("countries", None, AdminCountriesPage)
    GEOZONES = ("geo_zones", None, AdminGeozonesPage)
    USERS = ("users", None, AdminUsersPage)
