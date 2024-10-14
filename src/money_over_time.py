from src.movements_reader import *
from typing import Optional


def sum_total(entries: dict) -> dict:
    """
    Given all movement entries, all the dates are grouped
    together as keys and the amount of each one is summed
    as the value.
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
            separator: Optional[str] = ",",
            date_format: Optional[str] = "%d/%m/%Y",
            date_label: Optional[str] = "date",
            amount_label: Optional[str] = "amount",
            skip_label: Optional[str] = None,
            skip_value: Optional[str] = None,
    ):
        self.file_path = file_path
        self.separator = separator if separator is not None else ","
        self.date = {
            "label": date_label if date_label is not None else "date",
            "format": date_format if date_format is not None else "%d/%m/%Y",
            "index": -1,
        }
        self.amount = {
            "label": amount_label if amount_label is not None else "amount",
            "index": -1,
        }
        self.skip_label = {
            "value": skip_label if skip_label is not None else "",
            "index": -1,
            "match": skip_value if skip_value is not None else "",
        }

    def get_money_over_time(self) -> dict:
        """
        Reads all the movements in the specified file and returns a dict
        with the date of the movement as the key and the sum of the amount
        of all movements, for that day, as the value.
        """
        try:
            rows: list = get_lines_of_file(self.file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        try:
            column_headers = get_row_columns(self.separator, rows[0])
            self.date['index'] = get_index_of_column(self.date['label'], column_headers)
            self.amount['index'] = get_index_of_column(self.amount['label'], column_headers)

            if self.skip_label['value'] != "":
                self.skip_label['index'] = get_index_of_column(self.skip_label['value'], column_headers)
        except ValueError as e:
            raise ValueError(e)

        rows_without_header = rows[1:]
        rows_without_entries_to_skip = self.__remove_entries_to_skip(rows_without_header)

        entries: dict = get_entries_per_date(
            self.separator,
            rows_without_entries_to_skip,
            self.date['index'],
            self.date['format'],
            self.amount['index']
        )

        return sum_total(entries)

    def __remove_entries_to_skip(self, rows: list) -> list:
        """
        It's possible to exclude some movements based on some column value. For example,
        this may be useful when movements of an investment account should not be considered.
        """

        rows_without_entries_to_skip = []
        for row in rows:
            columns = get_row_columns(self.separator, row)

            # If the index of the "column to skip" has been set,
            # then the value in the cell of this row must be checked,
            # so that it's skipped if there's a match.
            if self.skip_label['index'] >= 0:
                skip: str = columns[self.skip_label['index']]
                if skip.lower() == self.skip_label['match'].lower():
                    continue

            rows_without_entries_to_skip.append(row)

        return rows_without_entries_to_skip