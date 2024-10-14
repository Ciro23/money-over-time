from io import StringIO
from typing import Optional
import pandas as pd
from src.movements_reader import *


def sum_total(entries: dict) -> dict:
    for date, amount in entries.items():
        entries[date] = round(amount, 2)

    return entries


class DiffOverTime:
    def __init__(
            self,
            source_file_path: str,
            reference_file_path: str,
            source_account: str,
            source_account_label: Optional[str] = "account",
            source_separator: Optional[str] = ",",
            source_date_format: Optional[str] = "%d/%m/%Y",
            source_date_label: Optional[str] = "date",
            source_amount_label: Optional[str] = "amount",
            reference_separator: Optional[str] = ",",
            reference_date_format: Optional[str] = "%d/%m/%Y",
            reference_date_label: Optional[str] = "date",
            reference_amount_label: Optional[str] = "amount",
    ):
        self.source_file_path = source_file_path
        self.source_separator = source_separator if source_separator is not None else ","
        self.source_account_label = source_account_label if source_account_label is not None else "account"
        self.source_account = source_account
        self.source_date = {
            "label": source_date_label if source_date_label is not None else "date",
            "format": source_date_format if source_date_format is not None else "%d/%m/%Y",
            "index": -1,
        }
        self.source_amount = {
            "label": source_amount_label if source_amount_label is not None else "amount",
            "index": -1,
        }

        self.reference_file_path = reference_file_path
        self.reference_separator = reference_separator if reference_separator is not None else ","
        self.reference_date = {
            "label": reference_date_label if reference_date_label is not None else "date",
            "format": reference_date_format if reference_date_format is not None else "%d/%m/%Y",
            "index": -1,
        }
        self.reference_amount = {
            "label": reference_amount_label if reference_amount_label is not None else "amount",
            "index": -1,
        }

    def get_diff_over_time(self):
        try:
            rows: list = get_lines_of_file(self.source_file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        try:
            column_headers = get_row_columns(self.source_separator, rows[0])
            self.source_date['index'] = get_index_of_column(self.source_date['label'], column_headers)
            self.source_amount['index'] = get_index_of_column(self.source_amount['label'], column_headers)
            account_index = get_index_of_column(self.source_account_label, column_headers)

            rows_without_header = rows[1:]
            rows_of_specified_account = self.__keep_only_entries_of_account(account_index, rows_without_header)

            source_entries: dict = get_entries_per_date(
                self.source_separator,
                rows_of_specified_account,
                self.source_date['index'],
                self.source_date['format'],
                self.source_amount['index']
            )
            source_entries = sum_total(source_entries)
        except ValueError as e:
            raise ValueError(e)

        try:
            if self.reference_file_path.endswith(".xlsx"):
                csv_data_in_memory = self.convert_xlsx_to_csv_in_memory(self.reference_file_path)
                pd.read_csv(csv_data_in_memory)
                rows = csv_data_in_memory.getvalue().splitlines()

                # Fuck pandas!
                self.reference_date['format'] = "%Y-%m-%d"
            else:
                rows: list = get_lines_of_file(self.reference_file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        try:
            column_headers = get_row_columns(self.reference_separator, rows[0])
            self.reference_date['index'] = get_index_of_column(self.reference_date['label'], column_headers)
            self.reference_amount['index'] = get_index_of_column(self.reference_amount['label'], column_headers)
            rows_without_header = rows[1:]

            reference_entries: dict = get_entries_per_date(
                self.reference_separator,
                rows_without_header,
                self.reference_date['index'],
                self.reference_date['format'],
                self.reference_amount['index']
            )
            reference_entries = sum_total(reference_entries)

            converted_reference_entries = {}
            for date_str, amount in reference_entries.items():
                # Convert the current date string to a datetime object
                date_obj = datetime.strptime(date_str, self.reference_date['format'])

                # Format it to the desired source date format
                formatted_date = date_obj.strftime(self.source_date['format'])

                # Add to the new dictionary
                converted_reference_entries[formatted_date] = amount

        except ValueError as e:
            raise ValueError(e)

        return self.__find_differences(source_entries, converted_reference_entries)

    def __keep_only_entries_of_account(self, account_index: int, rows: list) -> list:
        rows_of_account = []
        for row in rows:
            columns = get_row_columns(self.source_separator, row)

            skip: str = columns[account_index]
            if skip.lower() == self.source_account.lower():
                rows_of_account.append(row)

        return rows_of_account

    def __find_differences(self, dict1: dict, dict2: dict) -> dict:
        discrepancies = {}

        # Find entries with mismatching values for common dates
        for date in dict1:
            if date in dict2 and dict1[date] != dict2[date]:
                discrepancies[date] = {"dict1": dict1[date], "dict2": dict2[date]}

        # Find dates present in dict1 but missing in dict2
        for date in dict1:
            if date not in dict2:
                discrepancies[date] = {"dict1": dict1[date], "dict2": None}

        # Find dates present in dict2 but missing in dict1
        for date in dict2:
            if date not in dict1:
                discrepancies[date] = {"dict1": None, "dict2": dict2[date]}

        return sort_by_date_keys(self.source_date['format'], discrepancies)

    def convert_xlsx_to_csv_in_memory(self, xlsx_file: str):
        df = pd.read_excel(xlsx_file, engine='openpyxl')

        csv_buffer = StringIO()
        df.to_csv(csv_buffer, encoding='utf-8', index=False)

        csv_buffer.seek(0)
        return csv_buffer
