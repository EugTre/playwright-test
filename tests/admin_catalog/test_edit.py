import allure
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.admin_catalog import ProductEntity
from utils.pages import (
    AdminCatalogEditFormPage,
    AdminCatalogPage,
)
from utils.text_repository import messages
from constants import PRODUCT_IMAGES

from .metadata import EPIC, FEATURE, STORY


@allure.title("Existing Product may be edited")
@allure.epic(EPIC)
@allure.epic(FEATURE)
@allure.epic(STORY)
@pytest.mark.admin_category_page(AdminCategory.CATALOG)
@pytest.mark.new_product_options(add_images=PRODUCT_IMAGES)
def test_edit(
    admin_category_page: AdminCatalogPage,
    new_product: ProductEntity
):
    """Tests that existing product may be updated through UI"""

    with given("logged admin user is at Catalog page"):
        admin_category_page.reload()

    with given("there is created Product entity in the table"):
        row = admin_category_page.find_in_table(new_product, True)

    with when("user clicks Edit button for entity and opens Edit form"):
        edit_form: AdminCatalogEditFormPage = (
            admin_category_page.edit_entry(new_product, row_idx=row)
        )
        edit_form.verify_page()

    with when("user is updates data in form and saves it"):
        new_product.name = "X-TEST-CHANGED-X"
        new_product.short_desc = "Test updated description"
        new_product.full_desc = "New full description for test"
        new_product.sku = "e3e3e3"
        new_product.price = 999.99
        new_product.quantity = 10

        edit_form.remove_added_images()
        edit_form.fill_from_entity(new_product)
        edit_form.save()

    with then("user is navigated to Catalog page"):
        admin_category_page.verify_page()

    with then("edited data is displayed for product in the table"):
        admin_category_page.table_entry_data_should_match(new_product)

    with then("user sees success 'Changes saved' banner"):
        admin_category_page.banner_should_have_text(
            messages.get("General OnCreateSuccess")
        )

    with then("user can Edit product again and see new values in form"):
        edit_form = admin_category_page.edit_entry(new_product)
        edit_form.form_data_should_match_to(new_product)
