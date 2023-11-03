import allure  # type: ignore
import pytest

from constants import COUNTRIES_FIELDS_ANNOTATION_LINKS
from utils.bdd import given, then, when
from utils.models.admin_categories import AdminCategory
from utils.pages import AdminCountriesAddFormPage, AdminCountriesPage

from .metadata import EPIC, FEATURE, STORY


@allure.title("Create New Country form is available")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story(STORY)
@pytest.mark.admin_category_page(AdminCategory.COUNTRIES)
def test_form_verification(admin_category_page: AdminCountriesPage):
    """It is possible to access Create New Country from
    Admin -> Countries,
    - all fields and buttons of the form are present;
    - fields are anotated with external link to Wikipedia.org"""
    with given("logged in admin user is at Countries page"):
        pass

    with when("user clicks 'Create New Country' button"):
        form: AdminCountriesAddFormPage = admin_category_page.create_new()

    with then(
        "form 'Create New Country' is opened, "
        "contains expected fields and controls"
    ):
        form.verify_page()

    with then("form fields are annotated with link"):
        form.fields_should_be_annotated_with_links(
            COUNTRIES_FIELDS_ANNOTATION_LINKS
        )

    with then("annotation links opens in the new tab"):
        form.field_annotations_should_open_in_new_tabs()

    with then("clicking 'Cancel' returns user to Countries page"):
        form.cancel()
        admin_category_page.verify_page()
