from typing import Optional

from src.types.cell import Cell
from src.types.date_cell import DateCell
from src.types.entries import Movements
from src.movements_manager import change_movements_date_format, get_movements, exclude_all_except, \
    sort_movements_by_date


def get_diff_over_time(
        source_file_path: str,
        reference_file_path: str,
        source_delimiter: Optional[str] = None,
        source_including_cell: Optional[Cell] = None,
        source_date_cell: Optional[DateCell] = None,
        source_amount_label: Optional[str] = None,
        reference_delimiter: Optional[str] = None,
        reference_date_cell: Optional[DateCell] = None,
        reference_amount_label: Optional[str] = None,
):
    """
    Calculates the differences in financial entries over time
    between a source file and a reference one.
    This method is designed to help tracking differences in manually recorded
    financial movements against a reference dataset, allowing to identify potential
    accountability errors.
    """
    source_delimiter = "," if source_delimiter is None else source_delimiter
    source_date_cell = DateCell() if source_date_cell is None else source_date_cell
    source_amount_label = "amount" if source_amount_label is None else source_amount_label

    reference_delimiter = "," if reference_delimiter is None else reference_delimiter
    reference_date_cell = DateCell() if reference_date_cell is None else reference_date_cell
    reference_amount_label = "amount" if reference_amount_label is None else reference_amount_label

    source_movements = get_movements(
        source_file_path,
        source_delimiter,
        source_date_cell,
        source_amount_label,
        source_including_cell,
        exclude_all_except
    )

    reference_movements = get_movements(
        reference_file_path,
        reference_delimiter,
        reference_date_cell,
        reference_amount_label
    )

    if source_date_cell.date_format != reference_date_cell.date_format:
        reference_movements = change_movements_date_format(
            reference_date_cell.date_format,
            source_date_cell.date_format,
            reference_movements
        )

    differences_over_time = __find_differences(source_movements, reference_movements)
    return sort_movements_by_date(differences_over_time, source_date_cell.date_format)


def print_differences(differences_over_time: dict) -> None:
    print("Discrepancies found:")
    for date, values in differences_over_time.items():
        dict1_value = values['dict1']
        dict2_value = values['dict2']

        if dict1_value is None:
            print(f"# {date}"
                  f"\n   Source: Not available"
                  f"\n   Reference: {dict2_value:.2f}")
        elif dict2_value is None:
            print(f"# {date}"
                  f"\n   Source: {dict1_value:.2f}"
                  f"\n   Reference: Not available")
        else:
            print(
                f"# {date}"
                f"\n   Source: {dict1_value:.2f}"
                f"\n   Reference: {dict2_value:.2f}"
                f"\n   Difference: {dict2_value - dict1_value:.2f}")

        print("--------------------------------------")


def __find_differences(source_movements: Movements, reference_movements: Movements) -> dict:
    discrepancies = {}

    for date in source_movements:
        if date not in reference_movements:
            discrepancies[date] = {"dict1": source_movements[date], "dict2": None}
        elif date in reference_movements and source_movements[date] != reference_movements[date]:
            discrepancies[date] = {"dict1": source_movements[date], "dict2": reference_movements[date]}

    for date in reference_movements:
        if date not in source_movements:
            discrepancies[date] = {"dict1": None, "dict2": reference_movements[date]}

    return discrepancies
