import argparse


def parse_program_arguments() -> argparse.Namespace:
    program_desc = "A tool to manage and analyze financial records."
    parser = argparse.ArgumentParser(description=program_desc)

    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    plot_parser = subparsers.add_parser(
        "plot",
        help="Reads movements from a records file (CSV or XLSX) and shows a plot graph"
             " of the capital's trend over time."
    )
    diff_parser = subparsers.add_parser(
        "diff",
        help="Compares two sets of financial records (CSV or XLSX) to find discrepancies."
             " Useful to look for accounting errors."
    )

    __configure_plot_command(plot_parser)
    __configure_diff_command(diff_parser)

    return parser.parse_args()


def __configure_plot_command(parser) -> None:
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Path of CSV or XLSX (records file) containing all transactions"
    )
    parser.add_argument(
        "-d", "--delimiter",
        type=str,
        nargs="?",
        help="Delimiter used to distinguish a cell from another, default \",\""
    )
    parser.add_argument(
        "--date-format",
        type=str,
        nargs="?",
        help="Date format used in the records file, default \"%%d/%%m/%%Y\""
    )
    parser.add_argument(
        "--date-label",
        type=str,
        nargs="?",
        help="Date label used in the records file, default \"date\""
    )
    parser.add_argument(
        "--amount-label",
        type=str,
        nargs="?",
        help="Amount label used in the records file, default \"amount\""
    )
    parser.add_argument(
        "--exclude-label",
        type=str,
        nargs="?",
        help="The label of the column used to filter out some movements"
    )
    parser.add_argument(
        "--exclude-value",
        type=str,
        nargs="?",
        help="Based on the column label specified with \"--exclude-label\", all"
             " rows which cell matches this value are not considered"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Prints a more detailed error if something goes wrong while reading the file"
    )


def __configure_diff_command(parser) -> None:
    parser.add_argument(
        "--source-file",
        type=str,
        required=True,
        help="Path of CSV or XLSX (records file) containing all transactions"
    )
    parser.add_argument(
        "--source-delimiter",
        type=str,
        nargs="?",
        help="Delimiter used to distinguish a cell from another in the source records file, default \",\""
    )
    parser.add_argument(
        "--include-label",
        type=str,
        nargs="?",
        help="The label of the column used to filter in some movements, and exclude all the others"
    )
    parser.add_argument(
        "--include-value",
        type=str,
        nargs="?",
        help="Based on the column label specified with \"--include-label\", all"
             " rows which cell matches this value are the only ones considered"
    )
    parser.add_argument(
        "--source-date-format",
        type=str,
        nargs="?",
        help="Date format used in the source records file, default \"%%d/%%m/%%Y\""
    )
    parser.add_argument(
        "--source-date-label",
        type=str,
        nargs="?",
        help="Date label used in the source records file, default \"date\""
    )
    parser.add_argument(
        "--source-amount-label",
        type=str,
        nargs="?",
        help="Amount label used in the source records file, default \"amount\""
    )

    parser.add_argument(
        "--reference-file",
        type=str,
        required=True,
        help="Path of CSV or XLSX (records file) containing all transactions"
    )
    parser.add_argument(
        "--reference-delimiter",
        type=str,
        nargs="?",
        help="Delimiter used to distinguish a cell from another in the reference records file, default \",\""
    )
    parser.add_argument(
        "--reference-date-format",
        type=str,
        nargs="?",
        help="Date format used in the reference records file, default \"%%d/%%m/%%Y\""
    )
    parser.add_argument(
        "--reference-date-label",
        type=str,
        nargs="?",
        help="Date label used in the reference records file, default \"date\""
    )
    parser.add_argument(
        "--reference-amount-label",
        type=str,
        nargs="?",
        help="Amount label used in the reference records file, default \"amount\""
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Prints a more detailed error if something goes wrong while reading the files"
    )
