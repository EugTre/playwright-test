"""Admin category page (unspecified)"""
from typing import TYPE_CHECKING

import pytest
import allure
from playwright.sync_api import Page

from utils.models.base_entity import BackOfficeEntity
from utils.models.entry_lookup_strategy import (
    EntryLookupStrategy,
    EntryReadStrategy
)
from utils.components import AdminSideMenu, AdminTopMenu
from utils.elements import Title, Table

from .base_page import BasePage

if TYPE_CHECKING:
    from utils.models.admin_categories import AdminCategory


class AdminBasicCategoryPage(BasePage):
    """Admin category page (basic).
    Supports only minumal number of common elements.
    Use specific category pages for advanced use."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.header_title = Title(
            page, "#main #content .card-title", "Title of the category"
        )

        self.top_menu = AdminTopMenu(page)
        self.side_menu = AdminSideMenu(page)

        self.table = Table(
            page, "#main #content table",
            "Main Table"
        )

    @property
    def url(self):
        """Return page's path URL."""
        return "/admin"

    @property
    def header(self) -> str:
        """Page header text"""
        return ""

    @property
    def breadcrumbs(self) -> tuple[str]:
        """Tuple of page's top menu breadcrumbs"""
        return tuple()

    @property
    def entity_id_get_value_strategy(self) -> EntryReadStrategy:
        """Returns value get strategy for entity ID"""
        return EntryLookupStrategy(
            1, "id", "input", by_text=False, is_primary_key=True
        )

    @property
    def table_row_lookup_strategy(self) -> tuple[EntryLookupStrategy]:
        """Returns lookup strategy for category table."""
        return (self.entity_id_get_value_strategy, )

    @property
    def table_get_row_text_strategy(self) -> tuple[EntryReadStrategy]:
        """Returns get texts read strategy category table.
        Defaults to "table_row_lookup_strategy" property."""
        return self.table_row_lookup_strategy

    def _verify_page_items(self):
        self.side_menu.should_be_visible()
        self.top_menu.should_be_visible()
        self.header_title.should_be_visible()

    # --- Actions
    def change_category(self, category: "AdminCategory") -> BasePage:
        """Selects and clicks category item in side menu, and
        returns instance of basic category page (unspecified)"""
        return self.side_menu.change_category(category)

    def find_in_table(
        self, entity: BackOfficeEntity, update_entity_id: bool = False
    ) -> int:
        """Looks for given entity in the table.

        Args (exclusive):
            entity (BackOfficeEntity): entity to find.
            update_entity_id (bool, optional). flag to update given entity
            with found ID. Defaults to False.

        Returns:
            int: row index.
        """

        self.log(
            "Looking for entity like: %s",
            entity.get_lookup_params()
        )

        row_idx = self.table.find_entry(entity, self.table_row_lookup_strategy)
        self.log("Entity was found at row %s", row_idx)

        if update_entity_id:
            entity.entity_id = self.table.get_entry_texts(
                row_idx,
                (self.entity_id_get_value_strategy, )
            )[0]

        allure.attach(
            f"At Row {row_idx}. Entity: {entity}",
            "Entry Found", allure.attachment_type.TEXT
        )

        return row_idx

    def get_row_text_for_entity(self, entity: BackOfficeEntity) -> list[str]:
        """Returns texts from given row index.

        Args:
            entity (BackOfficeEntity): entity to look for.

        Returns:
            list[str]: texts of corresponding row, where each element
            is a separate column defined by self.table_get_row_text_strategy.
        """
        with allure.step("Entry is in table"):
            row_idx = self.find_in_table(
                entity, self.table_row_lookup_strategy
            )
            self.table.entry_should_be_visible(row_idx)

        table_data = self.table.get_entry_texts(
            row_idx, self.table_get_row_text_strategy
        )

        return table_data

    # --- Assertions
    def header_text_should_match(self, header: str | None = None):
        """Verifies that header of the page match to given.

        If no 'header' text was given -- header from page descriptor
        will be used"""
        if header is None:
            header = self.header
        self.log('Checking page Header to be equal to "%s"', header)
        self.header_title.should_have_text(header)

    def breadcrumbs_should_match(self, items: tuple | list | None = None):
        """Verifies that breadcrumbs of the page match to given.

        If no 'items' were given -- items from page descriptor
        will be used"""
        if items is None:
            items = self.breadcrumbs
        self.top_menu.breadcrumbs_should_match(items)

    @allure.step("Check that table entry matches to expected")
    def table_entry_data_should_match(self, entity: BackOfficeEntity):
        """Check that geozone metadata matches to expected"""
        assert self.get_row_text_for_entity(entity), \
            "No data found for entity!"

    @allure.step("Check that entry is missing in the table")
    def table_entry_should_be_missing(self, entity: BackOfficeEntity):
        """Checks that table is missing entry like given.
        Asserts otherwise.

        Args:
            entity (BackOfficeEntity): entity to look for.
        """
        with pytest.raises(
            ValueError, match=r"There is no row with data like.*"
        ):
            self.find_in_table(entity)
