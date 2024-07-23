import os
import unittest

from src.MoneyOverTime import MoneyOverTime


class MoneyOverTimeTest(unittest.TestCase):

    """
    Movements are read from a file with the default parameters (date label,
    date format, amount label, separator character...)
    """
    def test_default_parameters(self):
        file_path = os.path.join(os.path.dirname(__file__), 'movements_default.csv')
        money_over_time = MoneyOverTime(file_path)
        money_by_date = money_over_time.get_money_per_time()

        expected = {
            "15/06/2024": 65,
            "16/06/2024": 50,
            "17/06/2024": 1175,
            "01/07/2024": 1177,
        }
        self.assertEqual(expected, money_by_date)

    """
    The column labels should be case-insensitive.
    """
    def test_case_insensitive_columns(self):
        file_path = os.path.join(os.path.dirname(__file__), 'movements_default.csv')
        money_over_time = MoneyOverTime(
            file_path,
            date_label="DATE",
            amount_label="aMoUnT"
        )
        money_by_date = money_over_time.get_money_per_time()

        expected = {
            "15/06/2024": 65,
            "16/06/2024": 50,
            "17/06/2024": 1175,
            "01/07/2024": 1177,
        }
        self.assertEqual(expected, money_by_date)

    """
    Certain rows can be skipped if a given column value matches a discriminating
    word or phrase.
    """
    def test_skip_values(self):
        file_path = os.path.join(os.path.dirname(__file__), 'movements_default.csv')
        money_over_time = MoneyOverTime(file_path, skip_label="account", skip_value="cash")
        money_by_date = money_over_time.get_money_per_time()

        expected = {
            "16/06/2024": -15,
            "17/06/2024": 1470,
            "01/07/2024": 1460,
        }
        self.assertEqual(expected, money_by_date)


if __name__ == '__main__':
    unittest.main()
