"""Admin -> Geo Zones page"""
import allure
from playwright.sync_api import Page
from utils.models.admin_geozone import GeozoneEntity
from utils.elements import Input, Button, Select
from .admin_basic_category_page import AdminBasicCategoryPage


class AdminGeozonesFormPage(AdminBasicCategoryPage):
    """Admin -> Geo Zones page"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.save_button = Button(
            page, "#content .card-action button[name='save']",
            "Save"
        )
        self.cancel_button = Button(
            page, "#content .card-action button[name='cancel']",
            "Cancel"
        )

        self.code_field = Input(
            page, "#content form input[name='code']",
            "Code field"
        )
        self.name_field = Input(
            page, "#content form input[name='name']",
            "Name field"
        )
        self.desc_field = Input(
            page, "#content form input[name='description']",
            "Description field"
        )

        self.zone_country_select = Select(
            page, "#content form select[name*='country_code']",
            "Zones/Country dropdown"
        )
        self.zone_zones_field = Input(
            page, "#content form select[name*='zone_code']",
            "Zones/Zones field"
        )
        self.zone_city_field = Input(
            page, "#content form input[name='new_zone[city]']",
            "Zones/City field"
        )

        self.zone_add_button = Button(
            page, "#content form button[name='add']",
            "Add"
        )

    @property
    def url(self):
        return "/admin/?app=geo_zones&doc=edit_geo_zone&page=1"

    @property
    def header(self):
        return " Create New Geo Zone"

    @property
    def breadcrumbs(self):
        return ('Geo Zones', 'Create New Geo Zone')

    def _verify_page_items(self):
        super()._verify_page_items()
        self.cancel_button.should_be_visible()
        self.code_field.should_be_visible()
        self.name_field.should_be_visible()
        self.desc_field.should_be_visible()
        self.zone_add_button.should_be_visible()

    def get_country_option_names(self) -> list[tuple[str, str]]:
        """Returns list of options in format (value, name)
        except very first "-- Select --" option"""
        options_names = self.zone_country_select.get_option_names()[1:]
        return options_names

    @allure.step("Populate 'Create New Geo Zone' form with entity data")
    def fill_from_entity(self, entity: GeozoneEntity) -> None:
        """Fill form fields using given Geozone entity as
        a value"""
        self.code_field.click_and_fill(entity.code)
        self.name_field.click_and_fill(entity.name)
        self.desc_field.click_and_fill(entity.description)

        if not entity.zones:
            return

        for zone in entity.zones:
            with allure.step(f'Adding zone for country {zone.value}'):
                self.zone_country_select.click()
                self.zone_country_select.select_option(value=zone.value)
                self.zone_city_field.click_and_fill(zone.city)
                self.zone_add_button.click()

    @allure.step('Save form')
    def save(self) -> None:
        """Clicks save button at form"""
        self.save_button.click()

    # --- Assertions
    @allure.step("Check number of options in Country dropdown "
                 "to be equal to {size} (excluding '-- Select --')")
    def country_options_size_should_be(self, size: int) -> None:
        """Counts number of options in Country dropdown
        (excluding "-- Select --")"""
        self.zone_country_select.should_have_size_of(size + 1)
