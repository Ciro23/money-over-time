import argparse
import sys

import pandas as pd
import plotly.graph_objects as go

from MoneyOverTime import MoneyOverTime


def configure_plot_command(parser):
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="CSV containing all transactions path"
    )
    parser.add_argument(
        "-s", "--separator",
        type=str,
        nargs="?",
        help="Column separator, default \",\""
    )
    parser.add_argument(
        "--date_format",
        type=str,
        nargs="?",
        help="Date format used in the CSV file, default \"%%d/%%m/%%Y\""
    )
    parser.add_argument(
        "--date_label",
        type=str,
        nargs="?",
        help="Date label used in the CSV file, default \"date\""
    )
    parser.add_argument(
        "--amount_label",
        type=str,
        nargs="?",
        help="Amount label used in the CSV file, default \"amount\""
    )
    parser.add_argument(
        "--skip_label",
        type=str,
        nargs="?",
        help="The label of the column used to filter out some movements"
    )
    parser.add_argument(
        "--skip_value",
        type=str,
        nargs="?",
        help="Based on the column label specified with \"--skip_label\", all"
             " rows which cell matches this value are not considered"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Prints the actual Python error if something goes wrong while reading the file"
    )

def configure_diff_command(parser):
    parser.add_argument(
        "-s", "--source_file",
        type=str,
        help="CSV containing all transactions path"
    )
    parser.add_argument(
        "-a", "--account",
        type=str,
        help="The name of the account" # TODO: description
    )
    parser.add_argument(
        "--source_date_format",
        type=str,
        nargs="?",
        help="Date format used in the source CSV file, default \"%%d/%%m/%%Y\""
    )
    parser.add_argument(
        "--source_date_label",
        type=str,
        nargs="?",
        help="Date label used in the source CSV file, default \"date\""
    )
    parser.add_argument(
        "--source_amount_label",
        type=str,
        nargs="?",
        help="Amount label used in the source CSV file, default \"amount\""
    )

    parser.add_argument(
        "-r", "--reference_file",
        type=str,
        help="CSV containing all transactions path"
    )
    parser.add_argument(
        "--reference_date_format",
        type=str,
        nargs="?",
        help="Date format used in the reference CSV file, default \"%%d/%%m/%%Y\""
    )
    parser.add_argument(
        "--reference_date_label",
        type=str,
        nargs="?",
        help="Date label used in the reference CSV file, default \"date\""
    )
    parser.add_argument(
        "--reference_amount_label",
        type=str,
        nargs="?",
        help="Amount label used in the reference CSV file, default \"amount\""
    )

class Main:

    def __init__(self):
        program_desc = "A tool to manage and analyze financial records."
        self.parser = argparse.ArgumentParser(description=program_desc)

        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")
        plot_parser = subparsers.add_parser("plot", help="Reads movements from a CSV file and shows a plot graph of the capital's trend over time.")
        diff_parser = subparsers.add_parser("diff", help="Compares two sets of financial records to find discrepancies.")

        configure_plot_command(plot_parser)
        configure_diff_command(diff_parser)

        self.args = self.parser.parse_args()

        file = self.args.file
        if file is None:
            print("A file path is required. Use --help.")
            sys.exit(1)

        self.money = MoneyOverTime(
            file,
            self.args.separator,
            self.args.date_format,
            self.args.date_label,
            self.args.amount_label,
            self.args.skip_label,
            self.args.skip_value,
        )

    def execute_program(self):
        try:
            money_over_time: dict = self.money.get_money_over_time()
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

        self.__show_graph(money_over_time)

    def __show_graph(self, money_over_time: dict):
        """
        Plotly is used to display an interactive graph.
        """
        data_frame = pd.DataFrame(list(money_over_time.items()), columns=['date', 'value'])
        data_frame['date'] = pd.to_datetime(data_frame['date'], format=self.money.date['format'])

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


if __name__ == "__main__":
    main = Main()
    main.execute_program()
