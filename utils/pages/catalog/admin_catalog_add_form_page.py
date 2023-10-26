"""Admin / Catalog / Create New Product form"""
import allure

from playwright.sync_api import Page

from utils.models.admin_catalog import ProductEntity, ProductFormTab
from utils.elements import Button, Input, Textarea
from ..admin_basic_form_page import AdminBasicFormPage


class AdminCatalogAddFormPage(AdminBasicFormPage):
    """Represents Admin / Catalog / Create New Product form"""
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.active_tab = Button(
            page, "#content nav a.active",
            "Active Tab"
        )
        self.form_tabs = Button(
            page, "#content nav a[href='#tab-{name}']",
            "Form Tab"
        )

        self.general_name_input = Input(
            page, "#tab-general input[name='name[en]']",
            "General/Name"
        )
        self.general_price_input = Input(
            page, "#tab-general input[name='prices[USD]']",
            "General/Price"
        )
        self.general_sku_input = Input(
            page, "#tab-general input[name=sku]",
            "General/SKU"
        )
        self.general_add_image_button = Button(
            page, "#tab-general #images a.add",
            "General/Add Image"
        )

        self.general_new_image_last_input = Input(
            page,
            "#tab-general #images div.new-images "
            "div.image:last-child input",
            "General/Last New Image"
        )
        self.general_new_image_index_input = Input(
            page,
            "#tab-general #images div.new-images "
            "div.image:nth-child({idx}]) input",
            "General/New Image"
        )

        self.info_short_desc_input = Input(
            page, "#tab-information input[name*=short_description]",
            "Information/Short Description"
        )
        # TODO: Replace with click and send keys
        self.info_desc_input = Textarea(
            page, "#tab-information textarea[name^=description]",
            "Information/Description"
        )

        self.stock_quantity = Input(
            page, "#tab-stock tbody input[name=quantity]",
            "Stock/Quantity"
        )

    @property
    def url(self):
        return "/admin/?category_id=0&app=catalog&doc=edit_product"

    @property
    def name(self):
        return "Admin/Catalog/AddProductForm"

    @property
    def header(self):
        return "Create New Product"

    @property
    def breadcrumbs(self):
        return ("Catalog", "Create New Product")

    def _verify_page_items(self):
        super()._verify_page_items()
        self.save_button.should_be_visible()
        self.cancel_button.should_be_visible()
        self.active_tab.should_be_visible()
        self.general_name_input.should_be_visible()
        self.general_price_input.should_be_visible()
        self.general_sku_input.should_be_visible()
        self.general_add_image_button.should_be_visible()

    # --- Actions
    def fill_from_entity(self, entity: ProductEntity) -> None:
        """Fills required fields to create valid product
        available from Frontend"""

        self.log("Pupulating Create New Product form with data %s", entity)
        with allure.step(
            f'Populate "{self.header}" form with entity data'
        ):
            self.switch_tab(ProductFormTab.GENERAL)
            self.general_name_input.click_and_fill(entity.name)
            self.general_price_input.click_and_fill(entity.price)
            self.general_sku_input.click_and_fill(entity.sku)

            for img_path in entity.images:
                self.general_add_image_button.click()
                with self.page.expect_file_chooser() as fc:
                    self.general_new_image_last_input.click()

                chooser = fc.value
                chooser.set_files(img_path)

            self.switch_tab(ProductFormTab.INFORMATION)
            self.info_short_desc_input.click_and_fill(entity.short_desc)
            self.info_desc_input.click_and_fill(entity.full_desc)

            self.switch_tab(ProductFormTab.STOCK)
            self.stock_quantity.click_and_fill(entity.quantity)

        self.log("Form Create New Product populated")

    @allure.step('Switching form tab to "{tab_name}"')
    def switch_tab(self, tab_name: ProductFormTab) -> None:
        """Clicks tab selected by name"""
        tab_name_value = tab_name.value
        self.log('Clicking "%s" button on form', tab_name_value)
        self.form_tabs.click(name=tab_name_value)
