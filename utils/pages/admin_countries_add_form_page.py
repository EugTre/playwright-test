"""Admin -> Countries -> Create New Country page"""
from logging import WARNING

import pytest
import allure
from playwright.sync_api import Page, TimeoutError
from utils.elements import Button
from utils.components import LinkAnnotatedField
from .admin_basic_category_page import AdminBasicCategoryPage


class AdminCountriesAddFormPage(AdminBasicCategoryPage):
    """Admin -> Countries -> Create New Country page"""
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.save_button = Button(
            page, "#content .card-action button[name=save]",
            "Save"
        )
        self.cancel_button = Button(
            page, "#content .card-action button[name=cancel]",
            "Cancel"
        )

        self.satatus_enabled_button = Button(
            page, "form input[name=status][value=1]",
            "Enabled"
        )
        self.satatus_disabled_button = Button(
            page, "form input[name=status][value=0]",
            "Disabled"
        )

        self.iso_number_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=iso_code_1])",
            "Number (ISO Code)"
        )
        self.iso_code1_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=iso_code_2])",
            "Code (ISO Code)"
        )
        self.iso_code2_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=iso_code_3])",
            "Code (ISO Code)"
        )

        self.address_format_field = LinkAnnotatedField(
            page, "form div.form-group:has(textarea[name=address_format])",
            "Address Format",
            input_type="textarea",
            elements_selectors_override={"link": "a:last-child"}
        )
        self.tax_id_format_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=tax_id_format])",
            "Tax ID Format"
        )
        self.postcode_format_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=postcode_format])",
            "Postcode Format"
        )
        self.language_code_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=language_code])",
            "Language Code"
        )
        self.currency_code_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=currency_code])",
            "Currency Code"
        )
        self.phone_country_code_field = LinkAnnotatedField(
            page, "form div.form-group:has(input[name=phone_code])",
            "Phone Country Code"
        )

        # Collection of annotated fields (with links in label)
        self.fields_with_links = {
            "iso_code_1": self.iso_number_field,
            "iso_code_2": self.iso_code1_field,
            "iso_code_3": self.iso_code2_field,
            "address_format": self.address_format_field,
            "tax_id_format": self.tax_id_format_field,
            "postcode_format": self.postcode_format_field,
            "language_code": self.language_code_field,
            "currency_code": self.currency_code_field,
            "phone_code": self.phone_country_code_field
        }

    @property
    def url(self):
        return '/admin/?app=countries&doc=edit_country'

    @property
    def name(self):
        return "Admin/Countries/AddForm"

    @property
    def header(self):
        return "Create New Country"

    @property
    def breadcrumbs(self) -> tuple[str]:
        return ('Countries', 'Create New Country')

    def _verify_page_items(self):
        super()._verify_page_items()
        self.save_button.should_be_visible()
        self.cancel_button.should_be_visible()

        self.iso_number_field.should_be_visible()
        self.address_format_field.should_be_visible()

    # --- Actions
    @allure.step("Cancel form")
    def cancel(self):
        """Click Cancel button"""
        self.log("Exiting form by 'Cancel' button")
        self.cancel_button.click()

    # --- Assertions
    @allure.step("Check that fields have labels with links")
    def fields_should_be_annotated_with_links(
        self, expected_annotations: dict
    ):
        """Checks that form fields have labels with extrenal links,
        compares links to given map of links.

        Args:
            expected_annotations (dict): map of links where keys:
            'name' of the related input and value is a tuple of
            name and link.
        """
        self.log("Check fields annotations to have links")
        for input_name, expected_value in expected_annotations.items():
            field = self.fields_with_links.get(input_name)
            if not field:
                # Report mismatch, but do not stop test
                self.log(
                    'There is no labeled input with name "%s".',
                    input_name, level=WARNING
                )
                continue

            expected_label_text, expected_href = expected_value
            self.log('Field "%s", expected label=%s, href=%s',
                     input_name, expected_label_text, expected_href)

            with allure.step(f'Checking field "{input_name}"'):
                field.should_be_visible()
                field.should_have_label_text(expected_label_text)
                field.label_should_contain_link()
                field.label_link_should_have_value(expected_href)

    @allure.step("[Page] Check that external links annotations "
                 "are opened in new tabs")
    def field_annotations_should_open_in_new_tabs(self):
        """Clicks each field annotation link and checks that
        link opens a new tab"""
        self.log("Going to check that annotation links opens in new tab")
        for field in self.fields_with_links.values():
            try:
                with self.page.context.expect_page(timeout=2000) as page_info:
                    field.click_link()

            except TimeoutError:
                pytest.fail(
                    'No new page was opened while clicking link at '
                    f'field {field.name} (href={field.get_link_value()}!'
                )

            self.log("Closing newly opend tab")
            page_info.value.close()
