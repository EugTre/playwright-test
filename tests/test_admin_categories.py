"""
epic('Admin')
feature('Categories')
story('Categories are available')
"""

import pytest
import allure
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminMainPage, AdminBasicCategoryPage
from utils.bdd import given, when, then


@allure.epic('Admin')
@allure.feature('Categories')
@allure.story('Categories are available')
class TestAdminCategories:
    """Tests related to admin categories selection"""

    @allure.title("{category} is available and may be viewed")
    @pytest.mark.parametrize("category", (
        AdminCategory.APPEARANCE,
        AdminCategory.APPEARANCE_FAVICON,
        AdminCategory.CATALOG,
        AdminCategory.COUNTRIES,
        AdminCategory.GEOZONES
    ))
    def test_categories_available(self, category: AdminCategory,
                                  admin_main_page: AdminMainPage):
        """Tests that all admin categories are listed
        and may be navigated"""

        with given("logged admin at main page"):
            pass

        with when(f"admin navigates to category [{category}]"):
            subpage: AdminBasicCategoryPage = \
                admin_main_page.change_category(category)

        with then("category page is opened and category header is displayed"):
            subpage.verify_page()
            subpage.header_text_should_match()

        with then("breadcrumbs includes category"):
            subpage.breadcrumbs_should_match()
