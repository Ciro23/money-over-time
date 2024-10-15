import csv
from datetime import datetime
from io import StringIO

import pandas as pd


def get_lines_of_xlsx(file_path: str) -> list:
    df = pd.read_excel(file_path, engine='openpyxl')
    csv_buffer = StringIO()

    df.to_csv(csv_buffer, encoding='utf-8', index=False)
    csv_buffer.seek(0)

    pd.read_csv(csv_buffer)
    return csv_buffer.getvalue().splitlines()

def get_lines_of_file(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return file.read().splitlines()

def get_row_cells(separator: str, row: str) -> list:
    return next(csv.reader([row], delimiter=separator))

def get_index_of_cell(cell_value: str, cells: list) -> int:
    """
    It's necessary to retrieve the index of cells given their label, so users
    only need to memorize the human-readable value inside them.
    This method is case-insensitive.
    """

    index = 0
    for cell in cells:
        if cell.lower() == cell_value.lower():
            return index

        index += 1

    raise ValueError(f"Could not find the index of the cell with label '{cell_value}'"
                     " Check if the specified value match the one in the csv file.")

def get_entries_per_date(
        separator: str,
        rows: list,
        date_index: int,
        date_format: str,
        amount_index: int
) -> dict:
    amount_per_date: dict = {}
    for row in rows:
        columns = get_row_cells(separator, row)

        date = columns[date_index]
        amount = columns[amount_index]
        float_amount = float(amount)

        if date in amount_per_date:
            amount_per_date[date] += float_amount
        else:
            amount_per_date[date] = float_amount

    return sort_by_date_keys(date_format, amount_per_date)

def sort_by_date_keys(date_format: str, dictionary: dict) -> dict:
    """
    All movements must be sorted chronologically by the
    date they were made.
    """
    return dict(
        sorted(
            dictionary.items(),
            key=lambda x: datetime.strptime(x[0], date_format)
        )
    )
