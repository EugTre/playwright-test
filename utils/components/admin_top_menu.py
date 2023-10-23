"""Admin's page top strip menu - logout button, to frontend button"""
from playwright.sync_api import Page

from utils.elements import Button, List

from .base_component import BaseComponent


class AdminTopMenu(BaseComponent):
    """Admin's page top strip menu - logout button, to frontend button, etc."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.log_out_button = Button(
            page, "a[title='Sign Out']", "Log Out button"
        )
        self.frontend_button = Button(
            page, "a[title='Frontend']", "Frontend button"
        )
        self.breadcrumbs = List(page, ".breadcrumb li", "Breadcrumbs items")

    @property
    def name(self):
        return "Top Menu"

    def should_be_visible(self):
        self.log("Check that component is visible")

        self.log_out_button.should_be_visible()
        self.frontend_button.should_be_visible()

    def breadcrumbs_should_match(self, items: tuple | list):
        """Checks that breadcrumbs visible names match to
        given.

        Given names will be prepended with default nodes ('Dasboard')
        automatically.
        """
        self.log("Check breadcrumbs at top menu to contain %s", items)
        self.breadcrumbs.should_have_items(["Dashboard", *items])
