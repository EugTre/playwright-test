"""
epic('Admin')
feature('Categories')
story('Countries')
"""
import copy

import pytest
import allure
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminCountriesPage
from utils.bdd import given, when, then


@allure.epic('Admin')
@allure.feature('Categories')
@allure.story('Countries')
class TestAdminCategoriesCountries:
    """Tests related to Admin / Countries category"""

    @allure.title("List of countries is oredered (A-Z)")
    @pytest.mark.admin_category_page(AdminCategory.COUNTRIES)
    def test_order(self, admin_category_page: AdminCountriesPage):
        """Tests that countries at Admin -> Countries section
        are listed in A-Z order except:
         - Åland Islands (must be treated as 'Aland Islands')
         - Türkiye (must be treated as 'Turkie')."""

        with given("logged in admin is at Countries category"):
            pass

        with when("list of countries is loaded"):
            admin_category_page.verify_page()

        with then("list of countries is not empty and contain 243 items"):
            admin_category_page.country_list_size_should_be(243)

        with then("countries ordering is ascending with special rules"):
            # Special sorting rules
            rules = [
                ('Åland Islands', 'Aland Islands'),
                ('Türkiye', 'Turkiye')
            ]

            countries = admin_category_page.get_countries()
            sorted_countries = copy.copy(countries)

            # First replace original values with one from 'rule'
            # Then sort and revert original values
            for find_what, replace_with in rules:
                idx = sorted_countries.index(find_what)
                sorted_countries[idx] = replace_with

            sorted_countries.sort()
            for replace_with, find_what in rules:
                idx = sorted_countries.index(find_what)
                sorted_countries[idx] = replace_with

            assert countries == sorted_countries, \
                "Countries in the table are not A-Z ordered!"
