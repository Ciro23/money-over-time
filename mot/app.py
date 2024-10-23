import sys
from argparse import Namespace

from mot.diff_over_time import get_diff_over_time, print_differences
from mot.money_over_time import get_money_over_time, show_graph
from mot.types.cell import Cell
from mot.types.date_cell import DateCell, DEFAULT_DATE_LABEL, DEFAULT_DATE_FORMAT
from mot.program_arguments import parse_program_arguments


def run() -> None:
    args = parse_program_arguments()
    result = True
    if args.command == "plot":
        result = __run_money_over_time(args)
    elif args.command == "diff":
        result = __run_diff_over_time(args)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


def __run_money_over_time(args: Namespace) -> bool:
    date_cell = DateCell(
        DEFAULT_DATE_LABEL if args.date_label is None else args.date_label,
        DEFAULT_DATE_FORMAT if args.date_format is None else args.date_format
    )

    if args.exclude_label is None or args.exclude_value is None:
        excluding_cell = None
    else:
        excluding_cell = Cell(
            args.exclude_label,
            args.exclude_value
        )

    try:
        movements = get_money_over_time(
            args.file,
            args.delimiter,
            date_cell,
            args.amount_label,
            excluding_cell
        )
    except FileNotFoundError:
        print("File not found!")
        return False
    except ValueError as e:
        message = "Error reading the file, check if arguments are correct, use --help for more."
        if args.verbose:
            print(message, e)
        else:
            print(message)
        return False

    show_graph(movements, date_cell.date_format)
    return True


def __run_diff_over_time(args: Namespace) -> bool:
    source_date_cell = DateCell(
        DEFAULT_DATE_LABEL if args.source_date_label is None else args.source_date_label,
        DEFAULT_DATE_FORMAT if args.source_date_format is None else args.source_date_format
    )
    reference_date_cell = DateCell(
        DEFAULT_DATE_LABEL if args.reference_date_label is None else args.reference_date_label,
        DEFAULT_DATE_FORMAT if args.reference_date_format is None else args.reference_date_format
    )

    if args.include_label is None or args.include_value is None:
        including_cell = None
    else:
        including_cell = Cell(
            args.include_label,
            args.include_value
        )

    try:
        differences_over_time = get_diff_over_time(
            args.source_file,
            args.reference_file,
            args.source_delimiter,
            including_cell,
            source_date_cell,
            args.source_amount_label,
            args.reference_delimiter,
            reference_date_cell,
            args.reference_amount_label
        )
    except FileNotFoundError as e:
        message = "File not found!"
        if args.verbose:
            print(message, e)
        else:
            print(message)
        return False
    except ValueError as e:
        message = "Error reading the files, check if arguments are correct, use --help for more."
        if args.verbose:
            print(message, e)
        else:
            print(message)
        return False

    if len(differences_over_time) == 0:
        print("No differences found!")
    else:
        print_differences(differences_over_time, source_date_cell.date_format)
    return True
