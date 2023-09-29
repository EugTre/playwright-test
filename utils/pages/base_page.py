"""Base page class to inherit by other pages"""

from abc import ABC, abstractmethod

import allure
from playwright.sync_api import Page, Response, expect


class BasePage(ABC):
    """Basic class for page"""
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    @property
    @abstractmethod
    def url(self):
        """Return page's path URL."""
        return '/'

    @abstractmethod
    def verify_page(self):
        """Verifies that page's key content present"""

    @allure.step("Check that page's title is equal to {title}")
    def page_to_have_title(self, title: str) -> None:
        """Check that title of the page is equal to given.

        Args:
            title (str): expected title
        """
        expect(self.page).to_have_title(title)

    def visit(self, url: str = None) -> Response | None:
        """Navigates to page.

        Args:
            url (str, optional): URL to navigate to. If not given -
            page's specific default URL will be used.

        Returns:
            Response | None: result of get request to page URL.
        """

        url = self._full_url(url)
        with allure.step(f'Visiting {url}'):
            response = self.page.goto(
                url,
                wait_until='networkidle'
            )

            if url is None:
                # If visit invocked to navigate to current page
                # verifiy that page have expected elements
                self.verify_page()

        return response

    @allure.step('Reloading page {self.page.url}')
    def reload(self) -> Response | None:
        """Reloads current page.

        Returns:
            Response | None: result of get request to page URL.
        """
        return self.page.reload(wait_until="domcontentloaded")

    def _full_url(self, url: str = None) -> str:
        """Compose full URL from page base url and page's url passed in
        methods.

        Args:
            url (str, optional): path url. Page's URL will be used
            if no url given.

        Returns:
            str: full URL.
        """
        path_url = self.url if url is None else url
        return f'{self.base_url}{path_url}'
