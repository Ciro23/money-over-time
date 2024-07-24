import argparse

import pandas as pd
import plotly.graph_objects as go

from MoneyOverTime import MoneyOverTime


class Main:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.add_arguments()
        self.args = self.parser.parse_args()

        file = self.args.file
        if file is None:
            print("A file path is required. Use --help.")
            return

        self.money = MoneyOverTime(
            file,
            self.args.separator,
            self.args.date_format,
            self.args.date_label,
            self.args.amount_label,
            self.args.skip_label,
            self.args.skip_value,
        )

    def add_arguments(self):
        self.parser.add_argument(
            "--file",
            type=str,
            help="CSV containing all transactions path"
        )
        self.parser.add_argument(
            "--separator",
            type=str,
            nargs="?",
            help="Column separator, default \",\""
        )
        self.parser.add_argument(
            "--date_format",
            type=str,
            nargs="?",
            help="Date format used in the CSV file, default \"%%d/%%m/%%Y\""
        )
        self.parser.add_argument(
            "--date_label",
            type=str,
            nargs="?",
            help="Date label used in the CSV file, default \"date\""
        )
        self.parser.add_argument(
            "--amount_label",
            type=str,
            nargs="?",
            help="Amount label used in the CSV file, default \"amount\""
        )
        self.parser.add_argument(
            "--skip_label",
            type=str,
            nargs="?",
            help="The label of the column used to filter out some movements"
        )
        self.parser.add_argument(
            "--skip_value",
            type=str,
            nargs="?",
            help="Based on the column label specified with \"--skip_label\", all"
                 " rows which cell matches this value are not considered"
        )
        self.parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Prints the actual Python error if something goes wrong while reading the file"
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

        self.show_graph(money_over_time)

    def show_graph(self, money_over_time: dict):
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
