"""Admin -> Geo Zones page"""
import allure
from playwright.sync_api import Page
from utils.models.admin_geozone import GeozoneEntity, CountryZoneEntity
from utils.elements import Input, Button, Select, Table
from .admin_basic_category_page import AdminBasicCategoryPage


class AdminGeozonesAddFormPage(AdminBasicCategoryPage):
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
            "Code"
        )
        self.name_field = Input(
            page, "#content form input[name='name']",
            "Name"
        )
        self.desc_field = Input(
            page, "#content form input[name='description']",
            "Description"
        )

        self.zone_country_select = Select(
            page, "#content form select[name*='country_code']",
            "Zones/Country"
        )
        self.zone_zones_field = Input(
            page, "#content form select[name*='zone_code']",
            "Zones/Zones"
        )
        self.zone_city_field = Input(
            page, "#content form input[name='new_zone[city]']",
            "Zones/City"
        )

        self.zone_add_button = Button(
            page, "#content form button[name='add']",
            "Zones/Add"
        )
        self.zone_delete_button = Button(
            page, "#content tbody tr:nth-child({at_row}) td.text-end a",
            "Delete Zone"
        )

        self.zone_table = Table(
            page, "#content form table",
            "Zones"
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

    def get_added_countries_names(self):
        """Returns list of added countries from table"""
        return self.zone_table.get_rows_content(columns=(1,))

    def get_added_zones_values(self):
        """Returns values of added zones from Zones table"""
        return self.zone_table.evaluate_on_nested_elements(
            nested_locator="input[type='hidden']",
            callback="nodes => Array.prototype.map.call(nodes, e => e.value)"
        )

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

    @allure.step("Removing zones from table")
    def remove_zones(self, *zones: CountryZoneEntity) -> None:
        """Clicks 'Delete zone' button for selected zones.

        Args:
            *zones (CountryZoneEntity, optional): list of zones
            to find and delete. If non given - all zones will be deleted.
        """
        if not zones:
            with allure.step('Removing all zones'):
                rows_count = self.zone_table.count()
                for _ in range(rows_count):
                    self.zone_delete_button.click(at_row=1)

        row_values = self.get_added_zones_values()
        for zone in zones:
            removed = False
            for idx, values in enumerate(row_values):
                # Check both country and city, as same country, but
                # different cities are allowed
                if zone.value != values[1] or zone.city != values[3]:
                    continue
                with allure.step(
                    f'Removing zone {values[1]} (ID: {values[0]})'
                ):
                    self.zone_delete_button.click(at_row=idx + 1)
                    removed = True

            if not removed:
                with allure.step(f"Failed to find {zone} in the table"):
                    pass

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
