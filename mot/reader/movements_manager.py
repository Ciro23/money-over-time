from datetime import datetime
from typing import List, Optional, Callable, Dict, Any

from mot.types.cell import Cell
from mot.types.date_cell import DateCell
from mot.types.movements import Movements
from mot.reader.movements_parser import get_row_cells, read_lines_of_xlsx, read_lines_of_text_file, get_index_of_cell, \
    parse_movements


def get_movements(
        file_path: str,
        delimiter: str,
        date_cell: DateCell,
        amount_label: str,
        filtering_cell: Optional[Cell] = None,
        filter_callback: Optional[Callable[[int, str, str, List[str]], List[str]]] = None
) -> Movements:
    date_format = date_cell.date_format
    try:
        if file_path.endswith(".xlsx"):
            rows = read_lines_of_xlsx(file_path)
            date_format = "%Y-%m-%d"
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
            amount_index
        ),
        date_format
    )

    # Fixing pandas mistakes...
    if file_path.endswith(".xlsx"):
        movements = change_movements_date_format(date_format, date_cell.date_format, movements)

    return round_amounts(movements)


def change_movements_date_format(
        current_date_format: str,
        new_date_format: str,
        movements: Movements
) -> Movements:
    """
    This function is useful when working with two sets of movement entries, using
    different date formats, so that one can be adapted to the other.
    """
    movements_with_formatted_date = {}
    for date_str, amount in movements.items():
        date_obj = datetime.strptime(date_str, current_date_format)
        formatted_date = date_obj.strftime(new_date_format)
        movements_with_formatted_date[formatted_date] = amount

    return movements_with_formatted_date


def round_amounts(movements: Movements) -> Movements:
    """
    Each amount is rounded to 2 decimals.
    """
    for date, amount in movements.items():
        movements[date] = round(amount, 2)

    return movements


def round_and_sum_total(movements: Movements) -> Movements:
    """
    Given a dictionary of movement entries with dates as keys and amounts as values,
    this function calculates a cumulative total amount and updates each entry
    to reflect the running total up to that date.
    Each total is rounded to 2 decimals.
    """
    total = 0.0
    for date, amount in movements.items():
        total += amount
        movements[date] = round(total, 2)

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


def sort_dictionary_by_keys(dictionary: Dict[str, Any], date_format: str) -> Dict[str, Any]:
    """
    Sorts a dictionary, which uses dates as the keys, chronologically.
    """
    return dict(
        sorted(
            dictionary.items(),
            key=lambda x: datetime.strptime(x[0], date_format)
        )
    )
