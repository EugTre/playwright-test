"""Admin -> Catalog"""
import allure

from playwright.sync_api import Page
from utils.models.admin_catalog import ProductEntity
from utils.models.entry_lookup_strategy import EntryLookupStrategy
from utils.elements import Table, Button, Label
from ..admin_basic_category_page import AdminBasicCategoryPage
from .admin_catalog_add_form_page import AdminCatalogAddFormPage


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

        self.table = Table(
            page, "#content form table",
            "Products"
        )
        self.table.set_strategy(
            lookup=TABLE_STRATEGIES,
            texts=TABLE_STRATEGIES
        )
        self.crete_product_button = Button(
            page, "#content .card-action li:last-child a",
            "Create New Product"
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

    def _verify_page_items(self):
        super()._verify_page_items()
        self.crete_product_button.should_be_visible()
        self.table.should_be_visible()

    # --- Utilities
    def find_in_table(
        self,
        entity: ProductEntity,
        update_entity_id: bool = False
    ) -> int:
        """Returns geozone row index and data (id, name, zones counter)
        for row with given name in geozones table.

        Args (exclusive):
            entity (ProductEntity): entity to find.
            update_entity_id (bool, optional). flag to update given entity
            with found data. Defaults to False.

        Returns:
            tuple in format
            (row_idx: int, entity_id: str, name: str, zones_count: int)"""

        self.log(
            "Looking for Product like: %s",
            entity.get_lookup_params()
        )

        row_idx = self.table.find_entry(entity)
        self.log(row_idx)

        if update_entity_id:
            entity.entity_id = self.table.get_entry_texts(
                row_idx=row_idx,
                strategy=[
                    ID_LOOKUP_STRATEGY
                ]
            )[0]

        allure.attach(
            f"At Row {row_idx}. Entity: {entity}",
            "Entry Found", allure.attachment_type.TEXT
        )

        return row_idx

    # -- Actions
    @allure.step('Opening Create new product form')
    def open_create_product_form(self) -> AdminCatalogAddFormPage:
        """Click "Create New Product" button and
        return AdminCatalogAddFormPage"""
        self.crete_product_button.click()
        return AdminCatalogAddFormPage(self.page)

    # -- Asserts
    @allure.step("Check that product table data matches to expected")
    def table_entry_data_should_match(self, entity: ProductEntity):
        """Check that entry table data matches to expected"""
        with allure.step("Entry is in table"):
            row_idx = self.find_in_table(entity)
            self.table.entry_should_be_visible(row_idx)

        _, data_name, data_sku, data_price = \
            self.table.get_entry_texts(row_idx)

        with allure.step(f'Product name matches to "{entity.name}"'):
            assert entity.name == data_name, \
                'Name mismatches for ' \
                f'"{entity.name}" (ID: {entity.entity_id})'

        with allure.step(f'Product SKU matches to "{entity.sku}"'):
            assert entity.sku == data_sku, \
                'SKU value mismatches for ' \
                f'"{entity.name}" (ID: {entity.entity_id})'

        with allure.step(f'Product Price matches to "{entity.price}"'):
            assert str(entity.price) == data_price, \
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
