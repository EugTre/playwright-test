"""Admin's page top strip menu - logout button, to frontend button"""
from playwright.sync_api import Page
from utils.elements import Button
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

    def should_be_visible(self):
        self.log_out_button.should_be_visible()
        self.frontend_button.should_be_visible()
