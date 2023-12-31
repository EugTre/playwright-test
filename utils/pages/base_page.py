"""Base page class to inherit by other pages"""
import logging
from abc import ABC, abstractmethod

import allure  # type: ignore
from playwright.sync_api import Page, Response, expect


class BasePage(ABC):
    """Basic class for page"""

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    @abstractmethod
    def url(self):
        """Return page's path URL."""
        return "/"

    @property
    @abstractmethod
    def name(self):
        """Name of the page for logging"""
        return "Default Page"

    def log(self, msg: str, *args, level: int = logging.INFO):
        """Logs message"""
        logging.log(level, f"[Page: {self.name}] {msg}", *args)

    def verify_page(self):
        """Verifies that page's key content present as Allure step"""
        self.log("Verification started")

        with allure.step("Page is loaded"):
            self._verify_page_items()

        self.log("Verification success")

    @abstractmethod
    def _verify_page_items(self):
        """Verifies that page's key content present"""

    @allure.step("Check that page's title is equal to {title}")
    def page_to_have_title(self, title: str) -> None:
        """Check that title of the page is equal to given.

        Args:
            title (str): expected title
        """
        self.log('Cheking page title to be "%s"', title)
        expect(self.page).to_have_title(title)

    def visit(self, url: str | None = None) -> Response | None:
        """Navigates to page.

        Args:
            url (str, optional): URL to navigate to. If not given -
            page's specific default URL will be used.

        Returns:
            Response | None: result of get request to page URL.
        """

        target_url = url
        if target_url is None:
            target_url = self.url

        self.log("Visiting page with URL: %s", target_url)

        with allure.step(f"Visiting {target_url}"):
            response = self.page.goto(target_url, wait_until="networkidle")

        self.log("URL: %s is visited", target_url)

        return response

    def reload(self) -> Response | None:
        """Reloads current page.

        Returns:
            Response | None: result of get request to page URL.
        """
        self.log("Reloading current page (URL: %s)", self.page.url)

        with allure.step(f"Reloading page {self.page.url}"):
            response = self.page.reload(wait_until="domcontentloaded")

        self.log("Page (URL: %s) reloaded", self.page.url)
        return response

    @allure.step("Snapshot of page visually matches to expected")
    def should_match_snapshot(self) -> None:
        """Checks page snapshot (screenshot) to match to
        'golden' snapshot"""
        self.log("Checking visual snapshot of the page")
        assert_snapshot = getattr(self.page, "assert_snapshot")
        if assert_snapshot:
            assert_snapshot()
        # self.page.assert_snapshot()  # type: ignore[attr-defined]
