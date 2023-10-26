import allure
import pytest

from utils import helpers
from utils.bdd import given, then, when
from utils.models.base_entity import BackOfficeEntity
from utils.models.admin_categories import AdminCategory
from utils.models.admin_catalog import ProductEntity
from utils.pages import (
    AdminCatalogPage,
    AdminCatalogAddFormPage
)
from utils.text_repository import messages
from constants import PRODUCT_IMAGES


from .metadata import EPIC, FEATURE, STORY


@allure.title("New Product may be created")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.admin_category_page(AdminCategory.CATALOG)
def test_create(
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
            admin_category_page.create_new_product()
        )

    with when(
        "user fills 'Create New Product' form and "
        "adding several countries"
    ):
        product: ProductEntity = \
            helpers.generate_new_product_entity(
                add_images=PRODUCT_IMAGES
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
