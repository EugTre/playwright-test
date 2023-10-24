"""
epic('Admin')
feature('Categories')
story('Catalog')
"""

# TBD

import allure
import pytest

from utils import helpers
from utils.bdd import given, then, when
from utils.models.base_entity import BackOfficeEntity
from utils.models.admin_categories import AdminCategory
from utils.models.admin_catalog import ProductEntity
from utils.pages import (
    AdminCatalogPage,
    AdminCatalogAddFormPage,
    # AdminCaalogEditFormPage
)
from utils.text_repository import messages
from constants import PRODUCT_IMAGES


@allure.epic("Admin")
@allure.feature("Categories")
@allure.story("Catalog")
class TestAdminCategoriesCatalog:
    """Tests related to Admin / Catalog category"""

    @allure.title("Create New Prduct form is available")
    @pytest.mark.admin_category_page(AdminCategory.CATALOG)
    def test_form_verification(self, admin_category_page: AdminCatalogPage):
        """It is possible to access Create New Product from
        Admin -> Catalog page"""

        with given("logged in admin user is at Catalog page"):
            pass

        with when("user clicks 'Create New Product' button"):
            form: AdminCatalogAddFormPage = (
                admin_category_page.open_create_product_form()
            )

        with then(
            "form 'Create New Product' is opened, "
            "contains expected fields and controls"
        ):
            form.verify_page()

        with then("clicking 'Cancel' returns user to Catalog page"):
            form.cancel()
            admin_category_page.verify_page()

    @allure.title("New Product may be created")
    @pytest.mark.admin_category_page(AdminCategory.CATALOG)
    def test_create(
        self,
        admin_category_page: AdminCatalogPage,
        handle_entities: list[BackOfficeEntity]
    ):
        """It's possible to create new Product from Admin UI at
        Admin -> Catalog page;
        created product is listed in table;
        created product have valid name, SKU and price in table;
        link to product at frontpage is created and accessable
        """

        with given("logged in admin user is at Catalog page"):
            pass

        with when("user clicks 'Create New Product' button"):
            form: AdminCatalogAddFormPage = (
                admin_category_page.open_create_product_form()
            )

        with when(
            "user fills 'Create New Product' form and "
            "adding several countries"
        ):
            product: ProductEntity = \
                helpers.generate_new_product_entity(
                    images=PRODUCT_IMAGES
                )
            form.fill_from_entity(product)

        with when("user saves form"):
            form.save()

        with then("user is redirected to Catalog category page"):
            admin_category_page.verify_page()

        with then(
            "created product is in the list, have valid name and attributes"
        ):
            admin_category_page.find_in_table(product, True)
            handle_entities.append(product)

            admin_category_page.table_entry_data_should_match(product)

        with then("user sees success 'Changes saved' banner"):
            admin_category_page.banner_should_have_text(
                messages.get("General OnCreateSuccess")
            )

    @pytest.mark.new_product_options()
    def test_xxx(self, new_product):
        import logging
        logging.info('TEST')

    # @allure.title("Existing Product may be viewed")
    # @pytest.mark.admin_category_page(AdminCategory.CATALOG)
    # def test_view_created(
    #     self,
    #     admin_category_page: AdminCatalogPage,
    #     new_product: ProductEntity,
    # ):
    #     """Verifies that created entity may be viewed via Edit form,
    #     and values are match to previously saved"""

    #     with given("logged admin user is at Catalog page"):
    #         admin_category_page.reload()

    #     with given("there is created Geozone entity in the table"):
    #         row_idx, _, _, _ = admin_category_page.find_product(
    #             new_product, True
    #         )

    #     with when("user clicks Edit button for entity"):
    #         edit_form: AdminProductEditFormPage = (
    #             admin_category_page.edit_product(
    #                 row_id=row_idx, geozone=new_product
    #             )
    #         )

    #     with then("user is navigated to Edit Product form"):
    #         edit_form.verify_page()
    #         edit_form.url_should_contain_entity_id()

    #     with then("form is populated with expected data"):
    #         edit_form.data_should_match_to(new_product)


    # @allure.title("Existing Geo Zone may be edited")
    # @pytest.mark.admin_category_page(AdminCategory.CATALOG)
    # def test_edit(
    #     self,
    #     admin_category_page: AdminCatalogPage,
    #     new_product: ProductEntity,
    # ):
    #     """Tests that existing product may be updated through UI:
    #     - change NAME, DESCRIPTION, SHORT DESC, PRICE, QUANTITY
    #     - remove images
    #     - add new images"""

    #     with given("logged admin user is at Catalog page"):
    #         admin_category_page.reload()

    #     with given("there is created Geozone entity in the table"):
    #         admin_category_page.find_product(new_product, True)


    #     with when("user clicks Edit button for entity and opens Edit form"):
    #         edit_form: AdminProductEditFormPage = (
    #             admin_category_page.edit_product(new_product)
    #         )
    #         edit_form.verify_page()

    #     with when("user is updates data in form and saves it"):
    #         # Change zone data, and re-populate form
    #         new_product.code = "XTEST"
    #         new_product.description = "New Description"
    #         new_product.name = "XXX-edited-zone-name"
    #         new_product.zones = [
    #             CountryZoneEntity(value="AM", city="TownA"),
    #             CountryZoneEntity(value="AM", city="TownB"),
    #         ]

    #         edit_form.remove_zones()
    #         edit_form.fill_from_entity(new_product)

    #         edit_form.save()

    #     with then("user is navigated to Geozone page"):
    #         admin_category_page.verify_page()

    #     with then("edited name and number of zones is displayed for zone"):
    #         admin_category_page.geozone_metadata_should_match(new_product)

    #     with then("user sees success 'Changes saved' banner"):
    #         admin_category_page.banner_should_have_text(
    #             messages.get("General OnCreateSuccess")
    #         )

    #     with then("user can Edit zone again and see new values in Form"):
    #         edit_form = admin_category_page.edit_product(new_product)
    #         edit_form.data_should_match_to(new_product)

    # @allure.title("Existing Geo Zone may be deleted")
    # @pytest.mark.admin_category_page(AdminCategory.CATALOG)
    # def test_delete(
    #     self,
    #     admin_category_page: AdminCatalogPage,
    #     new_product: ProductEntity,
    # ):
    #     """Tests it is possible to Create New Product at
    #     Admin -> Geo Zones section"""

    #     with given("logged in admin user is at Catalog page"):
    #         admin_category_page.reload()

    #     with given("there is created Geozone entity in the table"):
    #         admin_category_page.find_item(new_product, True)

    #     with when("user clicks 'Edit' button for existing Geo Zone"):
    #         edit_page: AdminProductEditFormPage = (
    #             admin_category_page.edit_item(new_product)
    #         )

    #     with when("user is navigated to Edit Geo Zone page"):
    #         edit_page.verify_page()

    #     with when("user selects Delete and confirms deletion"):
    #         edit_page.delete(confirm=True)

    #     with then("user is redirected to Catalog page"):
    #         admin_category_page.verify_page()

    #     with then("user sees success 'Changes saved' banner"):
    #         admin_category_page.banner_should_have_text(
    #             messages.get("General OnCreateSuccess")
    #         )

    #     with then("deleted Geo Zone is not listed in table"):
    #         admin_category_page.item_in_table_should_be_missing(new_product)
