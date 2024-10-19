import pandas as pd
import plotly.graph_objects as go

from src.diff_over_time import DiffOverTime
from src.types.entries import Movements
from src.money_over_time import MoneyOverTime
from src.program_arguments import parse_program_arguments


def show_graph(date_format: str, movements: Movements):
    """
    Plotly is used to display an interactive graph in the default installed browser.
    """
    data_frame = pd.DataFrame(list(movements.items()), columns=['date', 'value'])
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
        self.args = parse_program_arguments()

    def execute_program(self):
        if self.args.command == "plot":
            self.__execute_money_over_time()
        elif self.args.command == "diff":
            self.__execute_diff_over_time()

    def __execute_money_over_time(self):
        money_over_time = MoneyOverTime(
            self.args.file,
            self.args.delimiter,
            self.args.date_format,
            self.args.date_label,
            self.args.amount_label,
            self.args.exclude_label,
            self.args.exclude_value,
        )

        try:
            movements = money_over_time.get_money_over_time()
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

        show_graph(money_over_time.date.date_format, movements)

    def __execute_diff_over_time(self):
        diff_over_time = DiffOverTime(
            self.args.source_file,
            self.args.reference_file,
            self.args.include_value,
            self.args.include_label,
            self.args.source_delimiter,
            self.args.source_date_format,
            self.args.source_date_label,
            self.args.source_amount_label,
            self.args.reference_delimiter,
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
