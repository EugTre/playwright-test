"""
Admin / Categories / Categories are available
"""

import allure
import pytest

from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminBasicCategoryPage, AdminMainPage


@allure.title("{category} is available and may be viewed")
@allure.epic("Admin")
@allure.feature("Categories")
@allure.story("Categories are available")
@pytest.mark.parametrize(
    "category",
    (
        AdminCategory.APPEARANCE,
        AdminCategory.APPEARANCE_FAVICON,
        AdminCategory.CATALOG,
        AdminCategory.COUNTRIES,
        AdminCategory.GEOZONES,
    ),
)
def test_categories_available(
    category: AdminCategory, admin_main_page: AdminMainPage
):
    """Tests that admin category may be navigated"""
    with given("logged admin at main page"):
        pass

    with when(f"admin navigates to category [{category}]"):
        subpage: AdminBasicCategoryPage = \
            admin_main_page.side_menu.change_category(category)

    with then("category page is opened and category header is displayed"):
        subpage.verify_page()
        subpage.header_text_should_match()

    with then("breadcrumbs includes category"):
        subpage.breadcrumbs_should_match()
