import pydoc
from datetime import date
from typing import Optional, Dict

from mot.types.cell import Cell
from mot.types.date_cell import DateCell
from mot.types.movements import Movements
from mot.reader.movements_manager import get_movements, exclude_all_except, \
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
) -> Dict[date, Dict[str, float]]:
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

    differences_over_time = __find_differences(source_movements, reference_movements)
    return sort_dictionary_by_keys(differences_over_time, reverse=True)


def print_differences(differences_over_time: Dict[date, Dict[str, float]], date_format: str) -> None:
    """
    Uses output pagination, like the "less" Unix command.
    :param differences_over_time: The content to display.
    :param date_format: The date format to use when printing the date of each difference.
    """
    content = ["Differences found:"]
    for movement_date, values in differences_over_time.items():
        source_value = values.get("source")
        reference_value = values.get("reference")

        if source_value is None:
            content.append(f"> {movement_date.strftime(date_format)}")
            content.append(f"   Source: Not available")
            content.append(f"   Reference: {reference_value:+.2f}")
        elif reference_value is None:
            content.append(f"> {movement_date.strftime(date_format)}")
            content.append(f"   Source: {source_value:+.2f}")
            content.append(f"   Reference: Not available")
        else:
            content.append(f"> {movement_date.strftime(date_format)}")
            content.append(f"   Source: {source_value:+.2f}")
            content.append(f"   Reference: {reference_value:+.2f}")
            content.append(f"   Diff. (ref - src): {reference_value - source_value:+.2f}")

        content.append("")

    content_str = "\n".join(content)
    pydoc.pager(content_str)


def __find_differences(
        source_movements: Movements,
        reference_movements: Movements
) -> Dict[date, Dict[str, float]]:
    discrepancies = {}

    for movement_date in source_movements:
        if movement_date not in reference_movements:
            discrepancies[movement_date] = {
                "source": source_movements[movement_date]
            }
        elif movement_date in reference_movements and source_movements[movement_date] != reference_movements[movement_date]:
            discrepancies[movement_date] = {
                "source": source_movements[movement_date],
                "reference": reference_movements[movement_date]
            }

    for movement_date in reference_movements:
        if movement_date not in source_movements:
            discrepancies[movement_date] = {
                "reference": reference_movements[movement_date]
            }

    return discrepancies
