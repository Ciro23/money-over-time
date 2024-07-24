import os
import unittest

from src.MoneyOverTime import MoneyOverTime


class MoneyOverTimeTest(unittest.TestCase):

    def test_default_parameters(self):
        """
        Movements are read from a file with the default parameters (date label,
        date format, amount label, separator character...)
        """
        file_path = os.path.join(os.path.dirname(__file__), 'movements_default.csv')
        money_over_time = MoneyOverTime(file_path)
        money_by_date = money_over_time.get_money_over_time()

        expected = {
            "15/06/2024": 65,
            "16/06/2024": 50,
            "17/06/2024": 1175,
            "01/07/2024": 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_case_insensitive_columns(self):
        """
        The column labels should be case-insensitive.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'movements_default.csv')
        money_over_time = MoneyOverTime(
            file_path,
            date_label="DATE",
            amount_label="aMoUnT"
        )
        money_by_date = money_over_time.get_money_over_time()

        expected = {
            "15/06/2024": 65,
            "16/06/2024": 50,
            "17/06/2024": 1175,
            "01/07/2024": 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_skip_values(self):
        """
        Certain rows can be skipped if a given column value matches a discriminating
        word or phrase.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'movements_default.csv')
        money_over_time = MoneyOverTime(file_path, skip_label="account", skip_value="cash")
        money_by_date = money_over_time.get_money_over_time()

        expected = {
            "16/06/2024": -15,
            "17/06/2024": 1470,
            "01/07/2024": 1460,
        }
        self.assertEqual(expected, money_by_date)

    def test_custom_properties(self):
        file_path = os.path.join(os.path.dirname(__file__), 'movements_custom_properties.csv')
        money_over_time = MoneyOverTime(
            file_path,
            separator=";",
            date_format="%m/%d/%Y",
            date_label="data",
            amount_label="importo",
        )
        money_by_date = money_over_time.get_money_over_time()

        expected = {
            "06/15/2024": 65,
            "06/16/2024": 50,
            "06/17/2024": 1175,
            "07/01/2024": 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_trailing_comma(self):
        """
        Trailing commas, at the end of the rows, used to cause errors when not specifying
        skip_value, as its default value is an empty string, and trailing commas cause
        an additional column to be considered with the value of an empty string, causing
        lots of rows to be wrongfully skipped.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'movements_trailing_comma.csv')
        money_over_time = MoneyOverTime(file_path)
        money_by_date = money_over_time.get_money_over_time()

        expected = {
            "15/06/2024": 65,
            "16/06/2024": 50,
            "17/06/2024": 1175,
            "01/07/2024": 1177,
        }
        self.assertEqual(expected, money_by_date)

    def test_comma_in_column_value(self):
        """
        Columns can contain the same separator character, as long as the whole column
        value is quoted. This case caused errors because the columns were split manually,
        instead of using a proper csv library.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'movements_comma_in_column_value.csv')
        money_over_time = MoneyOverTime(file_path)
        money_by_date = money_over_time.get_money_over_time()

        expected = {
            "15/06/2024": 65,
            "16/06/2024": 50,
        }
        self.assertEqual(expected, money_by_date)


if __name__ == '__main__':
    unittest.main()
