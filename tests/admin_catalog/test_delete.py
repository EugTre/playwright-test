import allure
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.admin_catalog import ProductEntity
from utils.pages import (
    AdminCatalogPage,
    AdminCatalogEditFormPage
)
from utils.text_repository import messages
from constants import PRODUCT_IMAGES


from .metadata import EPIC, FEATURE, STORY


@allure.title("Existing Product may be deleted")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.admin_category_page(AdminCategory.CATALOG)
@pytest.mark.new_product_options(add_images=PRODUCT_IMAGES)
def test_create(
    admin_category_page: AdminCatalogPage,
    new_product: ProductEntity
):
    """Tests it is possible to delete existing Product
    at Admin -> Catalog -> Edit Product page"""

    with given("logged in admin user is at Catalog page"):
        admin_category_page.reload()

    with given("there is created Product entity in the table"):
        row = admin_category_page.find_in_table(new_product, True)

    with when("user clicks 'Edit' button for existing Product"):
        edit_page: AdminCatalogEditFormPage = (
            admin_category_page.edit_entry(new_product, row)
        )

    with when("user is navigated to Edit Product page"):
        edit_page.verify_page()

    with when("user selects Delete and confirms deletion"):
        edit_page.delete(confirm=True)

    with then("user is redirected to Catalog page"):
        admin_category_page.verify_page()

    with then("user sees success 'Changes saved' banner"):
        admin_category_page.banner_should_have_text(
            messages.get("General OnCreateSuccess")
        )

    with then("deleted Product is not listed in table"):
        admin_category_page.table_entry_should_be_missing(new_product)
