from typing import Literal, Optional

import pandas as pd
import plotly.graph_objects as go # type: ignore

from mot.types.cell import Cell
from mot.types.date_cell import DateCell
from mot.types.movements import Movements
from mot.reader.movements_manager import exclude_all_except, get_movements, include_all_except, round_and_sum_total


def get_money_over_time(
        file_path: str,
        delimiter: Optional[str] = None,
        date_cell: Optional[DateCell] = None,
        amount_label: Optional[str] = None,
        filtering_cell: Optional[Cell] = None,
        filter_mode: Literal["in", "out"] = "in"
) -> Movements:
    """
    Reads all the movements in the specified file and returns a dict
    with the date of the movement as the key and the sum of the amount
    of all movements, for that day, as the value.
    """
    delimiter = "," if delimiter is None else delimiter
    date_cell = DateCell() if date_cell is None else date_cell
    amount_label = "amount" if amount_label is None else amount_label

    filter_callback = exclude_all_except
    if filter_mode == "out":
        filter_callback = include_all_except

    movements = get_movements(
        file_path,
        delimiter,
        date_cell,
        amount_label,
        filtering_cell,
        filter_callback
    )
    return round_and_sum_total(movements)


def show_graph(movements: Movements, date_format: str) -> None:
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
