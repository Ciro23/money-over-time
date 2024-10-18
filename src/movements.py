from datetime import datetime
from typing import Dict, List

from src.movements_reader import get_row_cells


def get_movement_entries(
        file_path: str,
        delimiter: str,
        date_cell: DateCell,
        amount_label: str,
        filtering_cell: Optional[Cell],
        filter_callback
):
    date_format = date_cell.date_format
    try:
        if file_path.endswith(".xlsx"):
            rows = get_lines_of_xlsx(file_path)
            date_format = "%Y-%m-%d"
        else:
            rows = get_lines_of_text_file(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)

    rows_without_header = rows[1:]

    try:
        column_headers = get_row_cells(delimiter, rows[0])
        date_index = get_index_of_cell(date_cell.label, column_headers)
        amount_index = get_index_of_cell(amount_label, column_headers)

        if filtering_cell is not None:
            filtering_cell_index = get_index_of_cell(filtering_cell.label, column_headers)
            rows_without_header = filter_callback(
                filtering_cell_index,
                filtering_cell.value,
                delimiter,
                rows_without_header
            )
    except ValueError as e:
        raise ValueError(e)

    entries = get_movement_entries_per_date(
        rows_without_header,
        delimiter,
        date_index,
        date_format,
        amount_index
    )

    # Fixing pandas mistakes...
    if file_path.endswith(".xlsx"):
        entries = change_entries_date_format(date_format, date_cell.date_format, entries)

    return round_amounts(entries)

def change_entries_date_format(
        current_date_format: str,
        new_date_format: str,
        entries: Dict[str, str]
) -> dict:
    """
    This function is useful when working with two sets of movement entries, using
    different date formats, so that one can be adapted to the other.
    """
    entries_with_formatted_date = {}
    for date_str, amount in entries.items():
        date_obj = datetime.strptime(date_str, current_date_format)
        formatted_date = date_obj.strftime(new_date_format)
        entries_with_formatted_date[formatted_date] = amount

    return entries_with_formatted_date

def remove_entries_to_skip(
        account_index: int,
        value_to_match: str,
        separator: str,
        rows: List[str]
) -> List[str]:
    """
    It's possible to exclude some movements based on some column value. For example,
    this may be useful when movements of an investment account should not be considered.
    """
    rows_without_entries_to_skip = []
    for row in rows:
        columns = get_row_cells(separator, row)

        # If the index of the "column to skip" has been set,
        # then the value in the cell of this row must be checked,
        # so that it's skipped if there's a match.
        if account_index >= 0:
            skip: str = columns[account_index]
            if skip.lower() == value_to_match.lower():
                continue

        rows_without_entries_to_skip.append(row)

    return rows_without_entries_to_skip

def keep_only_entries_of_account(
        account_index: int,
        value_to_match: str,
        separator: str,
        rows: List[str]
) -> List[str]:
    rows_of_account = []
    for row in rows:
        columns = get_row_cells(separator, row)

        skip: str = columns[account_index]
        if skip.lower() == value_to_match.lower():
            rows_of_account.append(row)

    return rows_of_account
