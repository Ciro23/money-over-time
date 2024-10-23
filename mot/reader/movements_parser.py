import csv
import warnings
from datetime import datetime
from io import StringIO
from typing import List

import pandas as pd

from mot.types.movements import Movements


def read_lines_of_xlsx(file_path: str) -> List[str]:
    """
    WARNING: all cells containing dates will be automatically converted
    using the format "%Y-%m-%d" by Pandas!
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df = pd.read_excel(file_path, engine='openpyxl')

    csv_buffer = StringIO()

    df.to_csv(csv_buffer, encoding='utf-8', index=False)
    csv_buffer.seek(0)

    pd.read_csv(csv_buffer)
    return csv_buffer.getvalue().splitlines()


def read_lines_of_text_file(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return file.read().splitlines()


def parse_movements(
        rows: List[str],
        delimiter: str,
        date_index: int,
        date_format: str,
        amount_index: int
) -> Movements:
    """
    After reading the movements from a CSV or XLSX file, it's necessary
    to parse them into a more useful format.
    :param rows: Each row is a string of comma separated values, containing
                 at least an amount and the date the movement was made.
    :param delimiter: Cells delimiter (usually "," or ";").
    :param date_index: Zero based index of the cell containing the date.
    :param date_format: The date format used inside the rows.
    :param amount_index: Zero based index of the cell containing the amount.
    :return: The parsed movements by the date they were made.
    """
    amount_per_date: Movements = {}
    for row in rows:
        columns = get_row_cells(delimiter, row)

        date_str = columns[date_index]
        date = datetime.strptime(date_str, date_format)

        amount = columns[amount_index]
        float_amount = float(amount)

        if date in amount_per_date:
            amount_per_date[date] += float_amount
        else:
            amount_per_date[date] = float_amount

    return amount_per_date


def get_row_cells(delimiter: str, row: str) -> List[str]:
    return next(csv.reader([row], delimiter=delimiter))


def get_index_of_cell(cell_value: str, cells: List[str]) -> int:
    """
    It's necessary to retrieve the index of cells given their value, so
    users only need to memorize the human-readable value inside them.
    This method is case-insensitive.
    """
    index = 0
    for cell in cells:
        if cell.lower() == cell_value.lower():
            return index

        index += 1

    raise ValueError(f"Could not find the index of the cell with value '{cell_value}'"
                     " Check if the specified value match the one in the CSV/XLSX file.")
