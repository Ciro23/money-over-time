from src.cell import Cell
from src.date_cell import DateCell
from src.movements import *
from src.movements_reader import *
from typing import Optional


def sum_total(entries: dict) -> dict:
    """
    Given a dictionary of movement entries with dates as keys and amounts as values,
    this function calculates a cumulative total amount and updates each entry
    to reflect the running total up to that date.
    """
    total = 0
    for date, amount in entries.items():
        total += amount
        entries[date] = round(total, 2)

    return entries


class MoneyOverTime:
    def __init__(
            self,
            file_path: str,
            separator: Optional[str] = None,
            date_format: Optional[str] = None,
            date_label: Optional[str] = None,
            amount_label: Optional[str] = None,
            skip_label: Optional[str] = None,
            skip_value: Optional[str] = None,
    ):
        self.file_path = file_path
        self.separator = separator if separator is not None else ","
        self.date = DateCell(
            date_label if date_label is not None else "date",
            date_format if date_format is not None else "%d/%m/%Y",
        )
        self.amount_label = amount_label if amount_label is not None else "amount"
        self.skip_cell = Cell(
            skip_label if skip_label is not None else "",
            skip_value if skip_value is not None else "",
        )

    def get_money_over_time(self) -> dict:
        """
        Reads all the movements in the specified file and returns a dict
        with the date of the movement as the key and the sum of the amount
        of all movements, for that day, as the value.
        """
        try:
            rows: list = get_lines_of_text_file(self.file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        rows_without_header = rows[1:]

        try:
            column_headers = get_row_cells(self.separator, rows[0])
            date_index = get_index_of_cell(self.date.label, column_headers)
            amount_index = get_index_of_cell(self.amount_label, column_headers)

            if self.skip_cell.value != "":
                skip_cell_index = get_index_of_cell(self.skip_cell.label, column_headers)
                rows_without_header = remove_entries_to_skip(
                    skip_cell_index,
                    self.skip_cell.value,
                    self.separator,
                    rows_without_header
                )
        except ValueError as e:
            raise ValueError(e)

        entries: dict = get_movement_entries_per_date(
            rows_without_header,
            self.separator,
            date_index,
            self.date.date_format,
            amount_index
        )

        return sum_total(entries)
