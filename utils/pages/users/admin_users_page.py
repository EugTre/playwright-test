"""Representation of Admin / Users page"""
from utils.models.entry_lookup_strategy import (
    EntryLookupStrategy,
    LookupStrategiesType
)

from ..admin_basic_category_page import AdminBasicCategoryPage


class AdminUsersPage(AdminBasicCategoryPage):
    """Admin / Users page"""
    @property
    def url(self):
        """Return page's path URL."""
        return "/admin/?app=users&doc=users"

    @property
    def name(self) -> str:
        return "Users"

    @property
    def header(self) -> str:
        """Page header text"""
        return "Users"

    @property
    def breadcrumbs(self) -> tuple[str, ...]:
        """Tuple of page's top menu breadcrumbs"""
        return tuple("Users",)

    @property
    def table_row_lookup_strategy(self) -> LookupStrategiesType:
        return (
            EntryLookupStrategy(
                1, "entity_id", "input", by_text=False, is_primary_key=True
            ),
            EntryLookupStrategy(4, "username", "a"),
            EntryLookupStrategy(7, "date_valid_from"),
            EntryLookupStrategy(8, "date_valid_to"),
        )
