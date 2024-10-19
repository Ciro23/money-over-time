from typing import Optional

from src.types.cell import Cell
from src.types.date_cell import DateCell
from src.types.entries import Movements
from src.movements import get_movements, include_all_except, round_and_sum_total


class MoneyOverTime:
    def __init__(
            self,
            file_path: str,
            separator: Optional[str] = None,
            date_format: Optional[str] = None,
            date_label: Optional[str] = None,
            amount_label: Optional[str] = None,
            skip_label: Optional[str] = None,
            skip_value: Optional[str] = None,
    ):
        self.file_path = file_path
        self.separator = separator if separator is not None else ","
        self.date = DateCell(
            date_label if date_label is not None else "date",
            date_format if date_format is not None else "%d/%m/%Y",
        )
        self.amount_label = amount_label if amount_label is not None else "amount"
        self.excluding_cell = Cell(
            skip_label if skip_label is not None else "",
            skip_value if skip_value is not None else "",
        )

    def get_money_over_time(self) -> Movements:
        """
        Reads all the movements in the specified file and returns a dict
        with the date of the movement as the key and the sum of the amount
        of all movements, for that day, as the value.
        """
        movements = get_movements(
            self.file_path,
            self.separator,
            self.date,
            self.amount_label,
            self.excluding_cell,
            include_all_except
        )
        return round_and_sum_total(movements)
