"""Admin -> Catalog"""
import allure  # type: ignore
from typing import cast

from playwright.sync_api import Page
from utils.models.admin_catalog import ProductEntity
from utils.models.entry_lookup_strategy import (
    EntryLookupStrategy,
    LookupStrategiesType
)
from utils.elements import Button, Label
from ..admin_basic_category_page import AdminBasicCategoryPage
from .admin_catalog_add_form_page import AdminCatalogAddFormPage
from .admin_catalog_edit_form_page import AdminCatalogEditFormPage


# Table Lookup/Read strategy params
ID_LOOKUP_STRATEGY = EntryLookupStrategy(
    column=1,
    field="id", selector="input",
    by_text=False,
    is_primary_key=True
)
TABLE_STRATEGIES = (
    ID_LOOKUP_STRATEGY,
    EntryLookupStrategy(column=4, field="name", selector="a"),
    EntryLookupStrategy(column=5, field="sku"),
    EntryLookupStrategy(
        column=6, field="price",
        # Remove currency tag before comparison
        apply_expression="value.substr(1)"
    )
)


class AdminCatalogPage(AdminBasicCategoryPage):
    """Admin -> Catalog"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.crete_product_button = Button(
            page, "#content .card-action li:last-child a",
            "Create New Product"
        )

        self.product_edit_button = Button(
            page, "#content form tbody tr:nth-child({row}) a.btn[title=Edit]",
            "Edit"
        )

        self.notification_banner = Label(
            page, ".alert-success", "Notification banner"
        )

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
        return ("Catalog",)

    @property
    def table_row_lookup_strategy(self) -> LookupStrategiesType:
        return (
            self.entity_id_get_value_strategy,
            EntryLookupStrategy(column=4, field="name", selector="a"),
            EntryLookupStrategy(column=5, field="sku"),
            EntryLookupStrategy(
                column=6, field="price",
                # Remove currency tag before comparison
                apply_expression="value.substr(1)"
            )
        )

    def _verify_page_items(self):
        super()._verify_page_items()
        self.crete_product_button.should_be_visible()
        self.table.should_be_visible()

    # -- Actions
    @allure.step('Opening Create new product form')
    def create_new_product(self) -> AdminCatalogAddFormPage:
        """Click "Create New Product" button and
        return AdminCatalogAddFormPage"""
        self.crete_product_button.click()
        return AdminCatalogAddFormPage(self.page)

    def edit_entry(
        self,
        entity: ProductEntity,
        row_idx: int | None = None,
    ) -> AdminCatalogEditFormPage:
        """Clickes Edit button for selected geozone (by id or by name)"""
        if entity is None and row_idx is None:
            raise ValueError(
                "Product identifier is not given "
                "(product entity or row index)!"
            )

        if not row_idx or not entity.entity_id:
            row_idx = self.find_in_table(entity, True)
            cast(int, row_idx)

        # Note:
        # Shift row_idx +1 from 0-based index of py-array
        # to 1-based of css selector
        self.product_edit_button.click(row=row_idx + 1)
        return AdminCatalogEditFormPage(
            self.page, cast(int, entity.entity_id), entity.name
        )

    # -- Asserts
    @allure.step("Check that product table data matches to expected")
    def table_entry_data_should_match(self, entity: ProductEntity):
        """Check that entry table data matches to expected"""

        self.log("Checking table entry to match %s", entity)
        _, data_name, data_sku, data_price = \
            self.get_row_text_for_entity(entity)

        with allure.step(f'Product name matches to "{entity.name}"'):
            assert entity.name == data_name, \
                'Name mismatches for ' \
                f'"{entity.name}" (ID: {entity.entity_id})'

        with allure.step(f'Product SKU matches to "{entity.sku}"'):
            assert entity.sku == data_sku, \
                'SKU value mismatches for ' \
                f'"{entity.name}" (ID: {entity.entity_id})'

        with allure.step(f'Product Price matches to "{entity.price}"'):
            assert f"{entity.price:.2f}" == data_price, \
                'Price value mismatches for ' \
                f'"{entity.name}" (ID: {entity.entity_id})'

    @allure.step(
        "Check that notification banner is displayed with text {text}"
    )
    def banner_should_have_text(self, text: str):
        """Checks that notification banner is visible
        and have given text"""
        self.notification_banner.should_be_visible()
        self.notification_banner.should_have_text(text)
