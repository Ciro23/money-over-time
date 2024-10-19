from typing import Optional

from src.types.cell import Cell
from src.types.date_cell import DateCell
from src.types.entries import Movements
from src.movements import change_movements_date_format, get_movements, exclude_all_except, \
    sort_movements_by_date


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
        between a source file and a reference one.
        This method is designed to help tracking differences in manually recorded
        financial movements against a reference dataset, allowing to identify potential
        accountability errors.
        """
        source_movements = get_movements(
            self.source_file_path,
            self.source_separator,
            self.source_date,
            self.source_amount_label,
            self.source_account,
            exclude_all_except
        )

        reference_movements = get_movements(
            self.reference_file_path,
            self.reference_separator,
            self.reference_date,
            self.reference_amount_label
        )

        if self.source_date.date_format != self.reference_date.date_format:
            reference_movements = change_movements_date_format(
                self.reference_date.date_format,
                self.source_date.date_format,
                reference_movements
            )

        return self.__find_differences(source_movements, reference_movements)

    def __find_differences(self, source_movements: Movements, reference_movements: Movements) -> dict:
        discrepancies = {}

        for date in source_movements:
            if date not in reference_movements:
                discrepancies[date] = {"dict1": source_movements[date], "dict2": None}
            elif date in reference_movements and source_movements[date] != reference_movements[date]:
                discrepancies[date] = {"dict1": source_movements[date], "dict2": reference_movements[date]}

        for date in reference_movements:
            if date not in source_movements:
                discrepancies[date] = {"dict1": None, "dict2": reference_movements[date]}

        return sort_movements_by_date(discrepancies, self.source_date.date_format)
