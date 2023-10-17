"""List item element"""

import allure
from playwright.sync_api import Locator, expect

from .base_element import BaseElement


class Table(BaseElement):
    """List element, representing group of <table> tag elements"""
    @property
    def type_of(self) -> str:
        return 'table'

    def get_rows(self, **locator_qualifiers) -> Locator:
        """Returns table's rows"""
        table = self.get_locator(**locator_qualifiers)
        return table.locator('tbody tr')

    def get_rows_content(self,
                         columns: list[int] | tuple[int] | None = None,
                         **locator_qualifiers) -> list[tuple[str]]:
        """Returns content of <td> blocks as tuples of values (strings)

        Args:
            columns (list[int] | tuple[int], optional): columns number to
            get data from. Defaults to None (all columns included).


        Returns:
            list[tuple[str]]: rows text data
        """
        table = self.get_locator(**locator_qualifiers)
        columns_count = table.locator('thead th').count()
        rows_content = table.locator('tbody td').all_text_contents()

        output = []
        for i in range(0, len(rows_content), columns_count):
            if not columns:
                row_data = rows_content[i:i + columns_count]
            else:
                # Filter by given column indicies
                row_data = []
                for j in columns:
                    row_data.append(rows_content[i+j])

            output.append(row_data)

        return output

    def should_have_size_of(self, size: int, **locator_qualifiers) -> None:
        """Checks that table contains exact number of elements"""
        rows = self.get_rows(**locator_qualifiers)
        with allure.step(f'{self.type_of.capitalize()} should have '
                         f'{size} items'):
            expect(rows).to_have_count(size)

    def shold_not_be_empty(self, **locator_qualifiers) -> None:
        """Checks that table is not empty"""
        tbody = self.get_locator(**locator_qualifiers).locator('tbody')
        with allure.step(f'{self.type_of.capitalize()} should have '
                         'at least 1 item'):
            expect(tbody).not_to_be_empty()
