import allure  # type: ignore
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.models.admin_catalog import ProductEntity
from utils.pages import (
    AdminCatalogPage,
    AdminCatalogEditFormPage
)
from constants import PRODUCT_IMAGES

from .metadata import EPIC, FEATURE, STORY


@allure.title("Existing Product may be viewed")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.admin_category_page(AdminCategory.CATALOG)
@pytest.mark.new_product_options(add_images=PRODUCT_IMAGES)
def test_view_created(
    admin_category_page: AdminCatalogPage,
    new_product: ProductEntity,
):
    """Verifies that created entity may be viewed via Edit form,
    and values are match to previously saved"""
    with given("logged admin user is at Catalog page"):
        admin_category_page.reload()

    with given("there is created Geozone entity in the table"):
        row_idx = admin_category_page.find_in_table(
            new_product, True
        )

    with when("user clicks Edit button for entity"):
        form: AdminCatalogEditFormPage = (
            admin_category_page.edit_entry(
                row_idx=row_idx, entity=new_product
            )
        )

    with then("user is navigated to Edit Product form"):
        form.verify_page()
        form.url_should_contain_entity_id()

    with then("form is populated with expected data"):
        form.form_data_should_match_to(new_product)

    with then("uploaded images are correctly displayed"):
        form.uploaded_images_should_match(new_product)
