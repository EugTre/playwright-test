import allure
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.pages import (
    AdminCatalogPage,
    AdminCatalogAddFormPage
)
from .metadata import EPIC, FEATURE, STORY


@allure.title("Create New Prduct form is available")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.admin_category_page(AdminCategory.CATALOG)
def test_form_verification(admin_category_page: AdminCatalogPage):
    """It is possible to access Create New Product from
    Admin -> Catalog page"""

    with given("logged in admin user is at Catalog page"):
        pass

    with when("user clicks 'Create New Product' button"):
        form: AdminCatalogAddFormPage = (
            admin_category_page.create_new_product()
        )

    with then(
        "form 'Create New Product' is opened, "
        "contains expected fields and controls"
    ):
        form.verify_page()

    with then("clicking 'Cancel' returns user to Catalog page"):
        form.cancel()
        admin_category_page.verify_page()
