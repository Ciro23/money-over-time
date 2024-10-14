import csv
from datetime import datetime
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
            rows: list = self.__get_lines_of_file()
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        try:
            entries: dict = self.__get_entries_per_date(rows)
        except ValueError as e:
            raise ValueError(e)

        return sum_total(entries)

    def __get_lines_of_file(self) -> list:
        with open(self.file_path, "r", encoding="utf-8-sig") as file:
            return file.read().splitlines()

    def __get_row_columns(self, row: str) -> list:
        return next(csv.reader([row], delimiter=self.separator))

    def __set_index_of_specific_columns(self, columns: list) -> None:
        """
        It's necessary to retrieve the index of the "amount" and "date"
        columns from their label. This method is case-insensitive.
        """
        index = 0

        for column in columns:
            column = column.lower()
            if column == self.date['label'].lower():
                self.date['index'] = index
            elif column == self.amount['label'].lower():
                self.amount['index'] = index
            elif column == self.skip_label['value'].lower() and column != "":
                # If no row should be skipped, columns containing empty strings must
                # not be considered, to avoid errors with trailing commas in the csv,
                # as the default value of self.skip_label['value'] is "".
                self.skip_label['index'] = index

            index += 1

        if self.date['index'] < 0 or self.amount['index'] < 0:
            raise ValueError("Could not find the index of the 'date' or 'amount' labels."
                             " Check if their specified label name match the ones in the csv file.")

    def __get_entries_per_date(self, rows: list) -> dict:
        amount_per_date: dict = {}
        execute_only_the_first_time: bool = True

        for row in rows:
            columns = self.__get_row_columns(row)

            if execute_only_the_first_time:
                execute_only_the_first_time = False
                try:
                    self.__set_index_of_specific_columns(columns)
                except ValueError as e:
                    raise ValueError(e)
                continue

            # If the index of the "column to skip" has been set,
            # then the value in the cell of this row must be checked,
            # so that it's skipped if there's a match.
            if self.skip_label['index'] >= 0:
                skip: str = columns[self.skip_label['index']]
                if skip.lower() == self.skip_label['match'].lower():
                    continue

            date = columns[self.date['index']]
            amount = columns[self.amount['index']]
            float_amount = float(amount)

            if date in amount_per_date:
                amount_per_date[date] += float_amount
            else:
                amount_per_date[date] = float_amount

        return self.__sort_by_date_keys(amount_per_date)

    def __sort_by_date_keys(self, dictionary: dict) -> dict:
        """
        All movements must be sorted chronologically by the
        date they were made.
        """
        return dict(
            sorted(
                dictionary.items(),
                key=lambda x: datetime.strptime(x[0], self.date['format'])
            )
        )
