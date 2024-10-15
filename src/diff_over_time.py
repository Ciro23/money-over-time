from typing import Optional

from src.cell import Cell
from src.date_cell import DateCell
from src.movements import *
from src.movements_reader import *


def round_amounts(entries: dict) -> dict:
    for date, amount in entries.items():
        entries[date] = round(amount, 2)

    return entries

def get_movement_entries(
        file_path: str,
        separator: str,
        date_cell: DateCell,
        amount_label: str,
        account: Optional[Cell]
):
    date_format = date_cell.date_format
    try:
        if file_path.endswith(".xlsx"):
            rows = get_lines_of_xlsx(file_path)
            date_format = "%Y-%m-%d"
        else:
            rows: list = get_lines_of_text_file(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)

    rows_without_header = rows[1:]

    try:
        column_headers = get_row_cells(separator, rows[0])
        date_index = get_index_of_cell(date_cell.label, column_headers)
        amount_index = get_index_of_cell(amount_label, column_headers)

        if account is not None:
            account_index = get_index_of_cell(account.label, column_headers)
            rows_without_header = keep_only_entries_of_account(
                account_index,
                account.value,
                separator,
                rows_without_header
            )
    except ValueError as e:
        raise ValueError(e)

    entries: dict = get_movement_entries_per_date(
        rows_without_header,
        separator,
        date_index,
        date_format,
        amount_index
    )

    # Fixing pandas mistakes...
    if file_path.endswith(".xlsx"):
        entries = change_entries_date_format(date_format, date_cell.date_format, entries)

    return round_amounts(entries)

class DiffOverTime:
    def __init__(
            self,
            source_file_path: str,
            reference_file_path: str,
            source_account: str,
            source_account_label: Optional[str] = None,
            source_separator: Optional[str] = None,
            source_date_format: Optional[str] = None,
            source_date_label: Optional[str] = None,
            source_amount_label: Optional[str] = None,
            reference_separator: Optional[str] = None,
            reference_date_format: Optional[str] = None,
            reference_date_label: Optional[str] = None,
            reference_amount_label: Optional[str] = None,
    ):
        self.source_file_path = source_file_path
        self.source_separator = source_separator if source_separator is not None else ","
        self.source_account = Cell(
            source_account_label if source_account_label is not None else "account",
            source_account
        )
        self.source_date = DateCell(
            source_date_label if source_date_label is not None else "date",
            source_date_format if source_date_format is not None else "%d/%m/%Y",
        )
        self.source_amount_label = source_amount_label if source_amount_label is not None else "amount"

        self.reference_file_path = reference_file_path
        self.reference_separator = reference_separator if reference_separator is not None else ","
        self.reference_date = DateCell(
            reference_date_label if reference_date_label is not None else "date",
            reference_date_format if reference_date_format is not None else "%d/%m/%Y",
        )
        self.reference_amount_label = reference_amount_label if reference_amount_label is not None else "amount"

    def get_diff_over_time(self):
        """
        Calculates the differences in financial entries over time
        between a source file and a reference file.
        This method is designed to help tracking differences in recorded
        financial movements against a reference dataset, allowing to identify potential
        accountability errors.
        """
        source_entries = get_movement_entries(
            self.source_file_path,
            self.source_separator,
            self.source_date,
            self.source_amount_label,
            self.source_account
        )

        reference_entries = get_movement_entries(
            self.reference_file_path,
            self.reference_separator,
            self.reference_date,
            self.reference_amount_label,
            None
        )

        if self.source_date.date_format != self.reference_date.date_format:
            reference_entries = change_entries_date_format(
                self.reference_date.date_format,
                self.source_date.date_format,
                reference_entries
            )

        return self.__find_differences(source_entries, reference_entries)

    def __find_differences(self, dict1: dict, dict2: dict) -> dict:
        discrepancies = {}

        for date in dict1:
            if date not in dict2:
                discrepancies[date] = {"dict1": dict1[date], "dict2": None}
            elif date in dict2 and dict1[date] != dict2[date]:
                discrepancies[date] = {"dict1": dict1[date], "dict2": dict2[date]}

        for date in dict2:
            if date not in dict1:
                discrepancies[date] = {"dict1": None, "dict2": dict2[date]}

        return sort_by_date_keys(self.source_date.date_format, discrepancies)
