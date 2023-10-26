"""Admin -> Product -> Edit Product page"""

import allure
from playwright.sync_api import Page, expect

from utils.models.admin_catalog import ProductEntity, ProductFormTab
from utils.elements import Button, Label


from .admin_catalog_add_form_page import AdminCatalogAddFormPage


class AdminCatalogEditFormPage(AdminCatalogAddFormPage):
    """Represents Admin -> Catalog -> Edit Product page"""
    def __init__(self, page: Page, entity_id: str, entity_name: str) -> None:
        super().__init__(page)

        self.entity_id = entity_id
        self.entity_name = entity_name

        self.delete_button = Button(
            page, "#content .card-action button[name='delete']", "Delete"
        )

        self.general_added_images = Label(
            page, "#tab-general #images div.images img",
            "Added Images"
        )
        self.general_remove_image_button = Button(
            page, "#tab-general div.images div.form-group:last-child a.remove",
            "Remove Image"
        )

    @property
    def url(self):
        return (
            "/admin/?app=catalog&doc=edit_product&category_id=0"
            f"&product_id={self.entity_id}"
        )

    @property
    def name(self):
        return "Admin/Catalog/EditForm"

    @property
    def header(self):
        return f"Edit Product: {self.entity_name}"

    @property
    def breadcrumbs(self):
        return ("Catalog", f"Edit Product: {self.entity_name}")

    def _verify_page_items(self):
        super()._verify_page_items()
        self.delete_button.should_be_visible()

    # --- Actions
    @allure.step("Deleting Product")
    def delete(self, confirm: bool = False):
        """Clicks 'Delete' button and optionally confirms in promt."""
        self.log("Deleting ")
        if confirm:
            self.page.on("dialog", lambda dialog: dialog.accept())

        self.delete_button.click()

    @allure.step("Removing zones from table")
    def remove_added_images(self) -> None:
        """Clicks 'Delete' button for each added image contol.
        """
        count = self.general_added_images.get_locator().count()
        self.log("Removing %s product image(s)", count)
        for _ in range(count):
            self.general_remove_image_button.click()

    # --- Assertions
    @allure.step("Check that page URL contains geo zone ID")
    def url_should_contain_entity_id(self):
        """Checks that pages url contains given entity_id"""
        expect(self.page).to_have_url(self.url)

    @allure.step(
        "Check that form contain data that matches to given geozone entity"
    )
    def form_data_should_match_to(self, entity: ProductEntity):
        """Checks that data in the fields is matching given
        geozone entity"""

        self.switch_tab(ProductFormTab.GENERAL)
        self.general_name_input.should_have_value(entity.name)
        self.general_price_input.should_have_value(f"{entity.price:.2f}")
        self.general_sku_input.should_have_value(entity.sku)
        if entity.images:
            self.general_remove_image_button.should_be_visible()
            expect(self.general_added_images.get_locator()).to_have_count(
                len(entity.images)
            )

        self.switch_tab(ProductFormTab.INFORMATION)
        self.info_short_desc_input.should_have_value(entity.short_desc)
        self.info_desc_input.should_have_value(entity.full_desc)

        self.switch_tab(ProductFormTab.STOCK)
        self.stock_quantity.should_have_value(str(entity.quantity))
