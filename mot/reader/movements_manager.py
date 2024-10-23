from datetime import date
from typing import List, Optional, Callable, Dict, Any

from mot.reader.movements_parser import get_row_cells, read_lines_of_xlsx, read_lines_of_text_file, get_index_of_cell, \
    parse_movements
from mot.types.cell import Cell
from mot.types.date_cell import DateCell
from mot.types.movements import Movements

FilterCallback = Callable[[int, str, str, List[str]], List[str]]
"""
The callback accepts:
    - 1: int -> The index of the cell to filter on.
    - 2: str -> The value to match for filtering.
    - 3: str -> The CSV/XLSX cells delimiter.
    - 4: List[str] -> the CSV/XLSX rows containing the movements to filter.
Returns the list of filtered rows.
"""

def get_movements(
        file_path: str,
        delimiter: str,
        date_cell: DateCell,
        amount_label: str,
        filtering_cell: Optional[Cell] = None,
        filter_callback: Optional[FilterCallback] = None
) -> Movements:
    """
    Reads the movements from a CSV/XLSX file.
    :param file_path: E.g. /home/ciro23/Documents/bank-movements.xlsx
    :param delimiter: CSV/XLSX cells delimiter (usually "," or ";").
    :param date_cell: Used to recognize the cell containing the date, given its label, and to
           correctly parse it using the right date format.
    :param amount_label: Used to recognize the cell containing the amount.
    :param filtering_cell: It's possible to filter movements based on the value of a specific cell
           of the CSV/XLSX file they're stored into.
    :param filter_callback: Based on the "filtering_cell", this callback specified the behaviour
           to filter in/out certain movements. Both this argument and "filtering_cell" must be specified
           to enable the filtering feature.
    :return:
    """
    try:
        if file_path.endswith(".xlsx"):
            rows = read_lines_of_xlsx(file_path)
            date_cell.date_format = "%Y-%m-%d"
        else:
            rows = read_lines_of_text_file(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)

    rows_without_header = rows[1:]

    try:
        column_headers = get_row_cells(delimiter, rows[0])
        date_index = get_index_of_cell(date_cell.label, column_headers)
        amount_index = get_index_of_cell(amount_label, column_headers)

        if filtering_cell is not None and filter_callback is not None:
            filtering_cell_index = get_index_of_cell(filtering_cell.label, column_headers)
            rows_without_header = filter_callback(
                filtering_cell_index,
                filtering_cell.value,
                delimiter,
                rows_without_header
            )
    except ValueError as e:
        raise ValueError(e)

    movements = sort_dictionary_by_keys(
        parse_movements(
            rows_without_header,
            delimiter,
            date_index,
            date_cell.date_format,
            amount_index
        )
    )

    return round_amounts(movements)


def round_amounts(movements: Movements) -> Movements:
    """
    Each amount is rounded to 2 decimals.
    """
    for movement_date, amount in movements.items():
        movements[movement_date] = round(amount, 2)

    return movements


def round_and_sum_total(movements: Movements) -> Movements:
    """
    Given a dictionary of movement entries with dates as keys and amounts as values,
    this function calculates a cumulative total amount and updates each entry
    to reflect the running total up to that date.
    Each total is rounded to 2 decimals.
    """
    total = 0.0
    for movement_date, amount in movements.items():
        total += amount
        movements[movement_date] = round(total, 2)

    return movements


def include_all_except(
        except_cell_index: int,
        value_to_match: str,
        delimiter: str,
        rows: List[str]
) -> List[str]:
    """
    This may be useful when movements of an investment account should not be considered.
    :param except_cell_index: The index of the cell that must be checked.
    :param value_to_match: The value to check against for the cell which index was specified.
    :param delimiter: Cells delimiter (usually "," or ";").
    :param rows: Movement rows read from the records file.
    :return: All movement rows except the ones which the specified cell matches a certain value.
    """
    filtered_rows = []
    for row in rows:
        columns = get_row_cells(delimiter, row)

        # If the index of the "column to skip" has been set,
        # then the value in the cell of this row must be checked,
        # so that it's skipped if there's a match.
        if except_cell_index >= 0:
            skip: str = columns[except_cell_index]
            if skip.lower() == value_to_match.lower():
                continue

        filtered_rows.append(row)

    return filtered_rows


def exclude_all_except(
        except_cell_index: int,
        value_to_match: str,
        delimiter: str,
        rows: List[str]
) -> List[str]:
    """
    This may be useful when only movements of a specific account should be
    considered.
    :param except_cell_index: The index of the cell that must be checked.
    :param value_to_match: The value to check against for the cell which index was specified.
    :param delimiter: Cells delimiter (usually "," or ";").
    :param rows: Movement rows read from the records file.
    :return: All movement rows which the specified cell does not match a certain value.
    """
    filtered_rows = []
    for row in rows:
        columns = get_row_cells(delimiter, row)

        skip: str = columns[except_cell_index]
        if skip.lower() == value_to_match.lower():
            filtered_rows.append(row)

    return filtered_rows


def sort_dictionary_by_keys(dictionary: Dict[date, Any], reverse: bool = False) -> Dict[date, Any]:
    """
    Sorts a dictionary, which uses dates as the keys.
    """
    return dict(
        sorted(
            dictionary.items(),
            key=lambda x: x[0],
            reverse=reverse
        )
    )
