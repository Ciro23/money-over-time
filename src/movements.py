from datetime import datetime

from src.movements_reader import get_row_cells


def change_entries_date_format(
        current_date_format: str,
        new_date_format: str,
        entries: dict
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
        rows: list
) -> list:
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
        rows: list
) -> list:
    rows_of_account = []
    for row in rows:
        columns = get_row_cells(separator, row)

        skip: str = columns[account_index]
        if skip.lower() == value_to_match.lower():
            rows_of_account.append(row)

    return rows_of_account
