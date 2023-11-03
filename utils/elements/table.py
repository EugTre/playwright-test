"""List item element"""
from typing import cast
import allure  # type: ignore
from playwright.sync_api import Locator, Page, expect

from utils.models.entry_lookup_strategy import (
    EntryReadStrategy,
    LookupStrategiesType,
    ReadStrategiesType
)
from utils.models.base_entity import BackOfficeEntity
from .base_element import BaseElement


# Snippet loops through rows, gets desired cells
# for specific elements text/values and compare to expected values.
# On success - returns index of a row; otherwise returns null (None).
JS_SNIPPET_FIND = """rows => {
  expected_data = [%s];
  let found = false;
  for (let i = 0; i < rows.length; ++i) {
    for (let j = 0; j < expected_data.length; ++j) {
      const [ sel, exp_val, by_text, expr, is_uid ] = expected_data[j];
      data_match = false;
      const element = rows[i].querySelector(sel);
      if (!element) { found = false; break; };
      let value = by_text ? element.innerText : element.value;
      if (expr) value = expr(value);
      if (exp_val != value) { found = false; break; };
      if (is_uid) return i;
      found = true;
    };
    if (found) return i;
  };
  return null;
};"""

# Snippet acquires 'tr' element and loops through desired td elements
# (according to provided strategy - index, nested element, etc)
# and collecting desired data (text or value), applying modifiers.
# Returns an array of gathered data.
JS_SNIPPET_GET_FROM_ROW = """row => {
  strategy = [%s];
  const result = [];
  for (let i = 0; i < strategy.length; ++i) {
    const [ sel, by_text, expr ] = strategy[i];
    const element = row.querySelector(sel);
    if (!element) { return null; };
    let value = by_text ? element.innerText : element.value;
    if (value && expr) value = expr(value);
    result.push(value);
  }
  return result;
};"""


class Table(BaseElement):
    """List element, representing group of <table> tag elements"""
    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page, locator, name)

    @property
    def type_of(self) -> str:
        return "table"

    def _convert_to_read_strategy(
        self,
        strategies: LookupStrategiesType | ReadStrategiesType
    ):
        """Convert  Lookup strategy entites to Read Strategy objects"""
        return tuple(
            st
            if isinstance(st, EntryReadStrategy) else
            st.to_read_strategy()
            for st in strategies
        )

    # --- Getters
    def get_rows_locator(self, **locator_qualifiers) -> Locator:
        """Returns table's rows"""
        table = self.get_locator(**locator_qualifiers)
        return table.locator("tbody tr")

    def get_row_locator(self, row_idx, **locator_qualifiers) -> Locator:
        """Returns table's row by zero-based row index"""
        table = self.get_locator(**locator_qualifiers)
        return table.locator(f"tbody tr:nth-child({row_idx+1})")

    def count_rows(self, **locator_qualifiers) -> int:
        """Returns number of rows in the table body"""
        return self.get_rows_locator(**locator_qualifiers).count()

    def find_entry(self, table_entry: BackOfficeEntity,
                   strategies: LookupStrategiesType,
                   **locator_qualifiers) -> int:
        """Find given target values using given lookup strategy
        and return row index, where entry was found.
        Allows to find entry in table by inner text of cells or
        by inner text or value of nested element in cell.

        Args:
            target_values (dict[str, str]): key-value pairs that maps
            expected values (value) to strategy by field name (key).
            strategies (optional, tuple[EntryLookupStrategy]): list of
            strategies to use. Defaults to strategies set with
            .set_default_strategies(lookup=...) method
            **locator_qualifiers (optional): kwargs for formatting
            base locator of the element.

        Raises:
            ValueError: if row was not found.

        Returns:
            int: row index (0-based) of found entry.
        """
        for st in strategies:
            if isinstance(st, EntryReadStrategy):
                raise RuntimeError(
                    "EntryReadStrategy should not be used "
                    "for Entry Lookup (.find_entry). "
                    "Use EntryLookupStrategy only!"
                )

        target_values = table_entry.get_lookup_params()

        if not any(target_values.values()):
            raise RuntimeError(
                f"Impossible to look up for null entity {table_entry}! "
                "At least 1 lookup field should not be None."
            )

        js_expr, strategy_data = self._preprare_lookup_expression(
            strategies, target_values
        )

        self.log(
            "Going to Find Entry in table using strategy data: %s",
            strategy_data
        )

        try:
            row_idx = self.get_rows_locator(**locator_qualifiers). \
                evaluate_all(js_expr)
        except Exception as exc:
            exc.add_note(
                "Error occured on attempting to find entry in table "
                f"using stratgy: {strategy_data}"
            )

        if row_idx is None:
            current_table_content = "\n".join([
                f"  {i:>3}) {cnt}"
                for i, cnt in enumerate(
                    self.get_rows_content(row_idx, **locator_qualifiers)
                )
            ])
            strategy_info = "\n  ".join([str(st) for st in strategies])
            raise ValueError(
                f"There is no row with data like {target_values}, "
                f"in the {self.name}!\n"
                "Table content:\n"
                f"  {current_table_content}\n"
                "Strategy:\n"
                f"  {strategy_info}"
            )

        self.log('Find Entry resulted in ROW IDX: %s', row_idx)
        return row_idx

    def get_entry_texts(
        self,
        row_idx: int,
        strategy: ReadStrategiesType | LookupStrategiesType,
        **locator_qualifiers
    ) -> list[str]:
        """Returns text from given row using given get_text_strategy.
        Strategy defines whas cells to check and how to retrieve values
        (e.g. from inner text, or from value of nested element).

        Args:
            strategies (optional,
            tuple[EntryReadStrategy, ...] | tuple[EntryLookupStrategy, ...] ):
            list of strategies to use. Defaults to strategies set with
            .set_default_strategies(texts=...) method
            **locator_qualifiers (optional): kwargs for formatting
            base locator of the element.

        Raises:
            ValueError: if row was not found.

        Returns:
            int: row index (0-based) of found entry.
        """
        strategy = self._convert_to_read_strategy(strategy)

        return self._get_entry_data(
            row_idx=row_idx,
            strategy=cast(ReadStrategiesType, strategy),
            **locator_qualifiers
        )

    def get_entry_values(
        self,
        row_idx: int,
        strategy: ReadStrategiesType,
        **locator_qualifiers
    ) -> list[str]:
        """Returns values from given row using given get_values_strategy.
        Strategy defines whas cells to check and how to retrieve values
        (e.g. from inner text, or from value of nested element).

        Args:
            strategies (optional,
            tuple[EntryReadStrategy | EntryLookupStrat]): list of
            strategies to use. Defaults to strategies set with
            .set_default_strategies(values=...) method.

            **locator_qualifiers (optional): kwargs for formatting
            base locator of the element.


        Raises:
            ValueError: if row was not found.

        Returns:
            int: row index (0-based) of found entry.
        """
        strategy = self._convert_to_read_strategy(strategy)

        return self._get_entry_data(
            row_idx=row_idx,
            strategy=strategy,
            **locator_qualifiers
        )

    def get_rows_content(
        self,
        columns: list[int] | tuple[int, ...] | None = None,
        **locator_qualifiers,
    ) -> list[list[str]]:
        """Returns inner text content of all <td> blocks as list
        of tuples of values (strings) grouped by rows.

        Args:
            columns (list[int] | tuple[int], optional): columns number to
            get data from. Defaults to None (all columns included).

        Returns:
            list[tuple[str]]: rows text data, where index is row index,
            and tuple - inner text values of each cell in a row.
        """
        table = self.get_locator(**locator_qualifiers)
        columns_count = table.locator("thead th").count()
        if columns is None:
            columns = tuple(range(columns_count))

        output = []
        rows_content = table.locator("tbody td").all_text_contents()
        for i in range(0, len(rows_content), columns_count):
            if not columns:
                row_data = rows_content[i: i + columns_count]
            else:
                # Filter by given column indicies
                row_data = []
                for j in columns:
                    row_data.append(rows_content[i + j])

            output.append([line.strip() for line in row_data])

        return output

    def _get_entry_data(
        self,
        row_idx: int,
        strategy: ReadStrategiesType,
        **locator_qualifiers
    ) -> list[str]:
        js_expr, strategy_data = self._prepare_read_expression(
            strategy
        )

        self.log(
            "Going to Get Entry Texts/Values from table "
            "using strategy data: %s",
            strategy_data
        )

        try:
            row_data = self.get_row_locator(row_idx, **locator_qualifiers). \
                evaluate(js_expr)
        except Exception as exc:
            exc.add_note(
                "Error occured on attempting to retrieve table's "
                f"row {row_idx} data using stratgy: {strategy_data}"
            )

        if row_data is None:
            raise ValueError(
                f"Failed to find or retrieve data from row {row_idx} "
                f"using strategy: \n{strategy_data}"
            )

        self.log(
            "Retrieved Entry Texts/Values: %s",
            row_data
        )

        return row_data

    def _preprare_lookup_expression(
        self,
        strategy: LookupStrategiesType,
        entity_fields_collection: dict[str, str | int]
    ):
        """Prepares JS expression using JS lookup snippet and
        given strategy and fields collection.

        Returns:
            tuple[str, list[str]]: ready to use JS code and prepared
            strategy data.
        """
        prepared_lookup_data = (
            st.prepare_strategy_data(entity_fields_collection)
            for st in strategy
        )

        strategy_data = [
            prepared
            for prepared in prepared_lookup_data
            if prepared is not None
        ]

        snippet = JS_SNIPPET_FIND % ",".join(strategy_data)
        return (snippet, strategy_data)

    def _prepare_read_expression(
        self,
        strategy: ReadStrategiesType,
    ) -> tuple[str, list[str]]:
        """Prepares JS expression using given snippet and strategy.
        If loadout was given - pass loadout values into a snippet.

        Returns:
            tuple[str, list[str]]: ready to use JS code and prepared
            strategy data.
        """
        prepared_read_data = (
            st.prepare_strategy_data() for st in strategy
        )

        strategy_data = [
            prepared
            for prepared in prepared_read_data
            if prepared is not None
        ]

        snippet = JS_SNIPPET_GET_FROM_ROW % ",".join(strategy_data)
        return (snippet, strategy_data)

    # --- Actions
    def evaluate_on_nested_elements(
        self, nested_locator: str, callback: str, **locator_qualifiers
    ) -> list[tuple[Locator]]:
        """Executes given JS code at each element found by
        given locator and returns result of the function
        callback.

        Args:
            nested_locator (str): locator inside table body's
            cell (<td>).
            callback (str): Javascript function to execute.

        Returns:
            list[tuple[Locator]]: _description_
        """

        table = self.get_locator(**locator_qualifiers)
        rows_count = table.locator("tbody tr").count()
        output = []

        for row_idx in range(rows_count):
            row_result = table.locator(
                f"tbody tr:nth-child({row_idx+1}) > td > {nested_locator}"
            ).evaluate_all(callback)
            output.append(row_result)

        return output

    # --- Assertions
    def should_have_size_of(self, size: int, **locator_qualifiers) -> None:
        """Checks that table contains exact number of elements"""
        rows = self.get_rows_locator(**locator_qualifiers)
        with allure.step(
            f"{self.type_of.capitalize()} should have " f"{size} items"
        ):
            expect(rows).to_have_count(size)

    def shold_be_empty(self, **locator_qualifiers) -> None:
        """Checks that table is empty"""
        tbody = self.get_locator(**locator_qualifiers).locator("tbody")
        with allure.step(
            f"{self.type_of.capitalize()} should have " "no items"
        ):
            expect(tbody).to_be_empty()

    def shold_not_be_empty(self, **locator_qualifiers) -> None:
        """Checks that table is not empty"""
        tbody = self.get_locator(**locator_qualifiers).locator("tbody")
        with allure.step(
            f"{self.type_of.capitalize()} should have " "at least 1 item"
        ):
            expect(tbody).not_to_be_empty()

    @allure.step("Entry at row {row_idx} should be visible")
    def entry_should_be_visible(self, row_idx):
        """Asserts that row and it's first and last cell are visibile."""
        row = self.get_row_locator(row_idx)
        expect(row).to_be_visible()
        expect(row.locator("td:first-child")).to_be_visible()
        expect(row.locator("td:last-child")).to_be_visible()
