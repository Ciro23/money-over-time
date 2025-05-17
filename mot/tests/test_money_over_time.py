import os
import unittest
from datetime import datetime

from mot.money_over_time import get_money_over_time
from mot.types.cell import Cell
from mot.types.date_cell import DateCell


class MoneyOverTimeTest(unittest.TestCase):

    def test_default_arguments(self):
        """
        Movements are read from a file with the default arguments (date label,
        date format, amount label, delimiter character...)
        """
        file_path = os.path.join(os.path.dirname(__file__), 'resources/movements_default.csv')
        money_by_date = get_money_over_time(file_path)

        date_format = "%d/%m/%Y"
        expected = {
            datetime.strptime("15/06/2024", date_format): 65,
            datetime.strptime("16/06/2024", date_format): 50,
            datetime.strptime("17/06/2024", date_format): 1175,
            datetime.strptime("01/07/2024", date_format): 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_case_insensitive_columns(self):
        """
        The column labels should be case-insensitive.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'resources/movements_default.csv')
        money_by_date = get_money_over_time(
            file_path,
            date_cell=DateCell("DATE"),
            amount_label="aMoUnT"
        )

        date_format = "%d/%m/%Y"
        expected = {
            datetime.strptime("15/06/2024", date_format): 65,
            datetime.strptime("16/06/2024", date_format): 50,
            datetime.strptime("17/06/2024", date_format): 1175,
            datetime.strptime("01/07/2024", date_format): 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_skip_values(self):
        """
        Certain rows can be skipped if a given column value matches a discriminating
        word or phrase.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'resources/movements_default.csv')
        money_by_date = get_money_over_time(file_path, filtering_cell=Cell("account", "cash"), filter_mode="out")

        date_format = "%d/%m/%Y"
        expected = {
            datetime.strptime("16/06/2024", date_format): -15,
            datetime.strptime("17/06/2024", date_format): 1470,
            datetime.strptime("01/07/2024", date_format): 1460,
        }
        self.assertEqual(expected, money_by_date)

    def test_custom_properties(self):
        file_path = os.path.join(os.path.dirname(__file__), 'resources/movements_custom_properties.csv')
        money_by_date = get_money_over_time(
            file_path,
            delimiter=";",
            date_cell=DateCell("data", "%m/%d/%Y"),
            amount_label="importo",
        )

        date_format = "%m/%d/%Y"
        expected = {
            datetime.strptime("06/15/2024", date_format): 65,
            datetime.strptime("06/16/2024", date_format): 50,
            datetime.strptime("06/17/2024", date_format): 1175,
            datetime.strptime("07/01/2024", date_format): 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_trailing_comma(self):
        """
        Trailing commas, at the end of the rows, used to cause errors when not specifying
        skip_value, as its default value is an empty string, and trailing commas cause
        an additional column to be considered with the value of an empty string, causing
        lots of rows to be wrongfully skipped.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'resources/movements_trailing_comma.csv')
        money_by_date = get_money_over_time(file_path)

        date_format = "%d/%m/%Y"
        expected = {
            datetime.strptime("15/06/2024", date_format): 65,
            datetime.strptime("16/06/2024", date_format): 50,
            datetime.strptime("17/06/2024", date_format): 1175,
            datetime.strptime("01/07/2024", date_format): 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_comma_in_column_value(self):
        """
        Columns can contain the same delimiter character, as long as the whole column
        value is quoted. This case caused errors because the columns were split manually,
        instead of using a proper csv library.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'resources/movements_comma_in_column_value.csv')
        money_by_date = get_money_over_time(file_path)

        date_format = "%d/%m/%Y"
        expected = {
            datetime.strptime("15/06/2024", date_format): 65,
            datetime.strptime("16/06/2024", date_format): 50,
        }
        self.assertEqual(expected, money_by_date)


if __name__ == '__main__':
    unittest.main()
