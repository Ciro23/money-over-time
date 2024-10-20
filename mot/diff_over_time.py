from typing import Optional, Dict

from mot.types.cell import Cell
from mot.types.date_cell import DateCell
from mot.types.movements import Movements
from mot.reader.movements_manager import change_movements_date_format, get_movements, exclude_all_except, \
    sort_dictionary_by_keys


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
) -> Dict[str, Dict[str, float]]:
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
    return sort_dictionary_by_keys(differences_over_time, source_date_cell.date_format)


def print_differences(differences_over_time: Dict[str, Dict[str, float]]) -> None:
    print("Differences found:")
    for date, values in differences_over_time.items():
        source_value = values.get("source")
        reference_value = values.get("reference")

        if source_value is None:
            print(f"# {date}"
                  f"\n   Source: Not available"
                  f"\n   Reference: {reference_value:+.2f}")
        elif reference_value is None:
            print(f"# {date}"
                  f"\n   Source: {source_value:+.2f}"
                  f"\n   Reference: Not available")
        else:
            print(
                f"# {date}"
                f"\n   Source: {source_value:+.2f}"
                f"\n   Reference: {reference_value:+.2f}"
                f"\n   Diff. (ref - src): {reference_value - source_value:+.2f}")

        print("--------------------------------------")


def __find_differences(
        source_movements: Movements,
        reference_movements: Movements
) -> Dict[str, Dict[str, float]]:
    discrepancies = {}

    for date in source_movements:
        if date not in reference_movements:
            discrepancies[date] = {"source": source_movements[date]}
        elif date in reference_movements and source_movements[date] != reference_movements[date]:
            discrepancies[date] = {"source": source_movements[date], "reference": reference_movements[date]}

    for date in reference_movements:
        if date not in source_movements:
            discrepancies[date] = {"reference": reference_movements[date]}

    return discrepancies
