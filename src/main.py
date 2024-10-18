import argparse
from typing import Dict

import pandas as pd
import plotly.graph_objects as go

from src.diff_over_time import DiffOverTime
from src.money_over_time import MoneyOverTime


def configure_plot_command(parser):
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="CSV containing all transactions path"
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
        help="Prints the actual Python error if something goes wrong while reading the file"
    )

def configure_diff_command(parser):
    parser.add_argument(
        "--source_file",
        type=str,
        required=True,
        help="CSV containing all transactions path"
    )
    parser.add_argument(
        "--source-delimiter",
        type=str,
        nargs="?",
        help="Delimiter used to distinguish a cell from another in the source file, default \",\""
    )
    parser.add_argument(
        "--include-label",
        type=str,
        help="The label of the column used to filter in some movements, and exclude all the others"
    )
    parser.add_argument(
        "--include-value",
        type=str,
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
        "-r", "--reference-file",
        type=str,
        required=True,
        help="CSV containing all transactions path"
    )
    parser.add_argument(
        "--reference-delimiter",
        type=str,
        nargs="?",
        help="Delimiter used to distinguish a cell from another in the reference file, default \",\""
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
        help="Prints the actual Python error if something goes wrong while reading the files"
    )


def show_graph(date_format: str, money_over_time: Dict[str, str]):
    """
    Plotly is used to display an interactive graph in the default installed browser.
    """
    data_frame = pd.DataFrame(list(money_over_time.items()), columns=['date', 'value'])
    data_frame['date'] = pd.to_datetime(data_frame['date'], format=date_format)

    data_frame = data_frame.sort_values(by='date')
    plot_graph = go.Figure()
    plot_graph.add_trace(
        go.Scatter(
            x=data_frame['date'],
            y=data_frame['value'],
            mode='lines+markers',
            name='Value',
            hovertemplate='<b>Date</b>: %{x}<br><b>Amount</b>: %{y}<extra></extra>',
        )
    )
    plot_graph.update_layout(
        title='Money over time',
        xaxis_title='Date',
        yaxis_title='Amount',
        hovermode='x unified',
    )

    plot_graph.show()


class Main:

    def __init__(self):
        program_desc = "A tool to manage and analyze financial records."
        self.parser = argparse.ArgumentParser(description=program_desc)

        subparsers = self.parser.add_subparsers(dest="command", help="Available commands", required=True)
        plot_parser = subparsers.add_parser(
            "plot",
            help="Reads movements from a records file (CSV or XLSX) and shows a plot graph of the capital's trend over time."
        )
        diff_parser = subparsers.add_parser(
            "diff",
            help="Compares two sets of financial records (CSV or XLSX) to find discrepancies."
        )

        configure_plot_command(plot_parser)
        configure_diff_command(diff_parser)

        self.args = self.parser.parse_args()

    def execute_program(self):
        if self.args.command == "plot":
            self.__execute_money_over_time()
        elif self.args.command == "diff":
            self.__execute_diff_over_time()

    def __execute_money_over_time(self):
        money_over_time = MoneyOverTime(
            self.args.file,
            self.args.separator,
            self.args.date_format,
            self.args.date_label,
            self.args.amount_label,
            self.args.skip_label,
            self.args.skip_value,
        )

        try:
            amount_of_money_over_time = money_over_time.get_money_over_time()
        except FileNotFoundError:
            print("File not found!")
            return
        except ValueError as e:
            message = "Error reading the file, check if parameters are correct, use --help for more."
            if self.args.verbose:
                print(message, e)
            else:
                print(message)
            return

        show_graph(money_over_time.date.date_format, amount_of_money_over_time)

    def __execute_diff_over_time(self):
        diff_over_time = DiffOverTime(
            self.args.source_file,
            self.args.reference_file,
            self.args.account,
            self.args.account_label,
            self.args.source_separator,
            self.args.source_date_format,
            self.args.source_date_label,
            self.args.source_amount_label,
            self.args.reference_separator,
            self.args.reference_date_format,
            self.args.reference_date_label,
            self.args.reference_amount_label
        )

        try:
            differences_over_time = diff_over_time.get_diff_over_time()
        except FileNotFoundError as e:
            message = "File not found!"
            print(message)
            if self.args.verbose:
                print(message, e)
            else:
                print(message)
            return
        except ValueError as e:
            message = "Error reading the files, check if parameters are correct, use --help for more."
            if self.args.verbose:
                print(message, e)
            else:
                print(message)
            return

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


if __name__ == "__main__":
    main = Main()
    main.execute_program()
