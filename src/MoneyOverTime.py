import matplotlib.pyplot as plt
from datetime import datetime
import argparse


class MoneyOverTime:
    file_path = "/Users/tino/Downloads/monefy-2022-10-21_09-12-11.csv"
    date_format = "%d/%m/%Y"
    date_label = {
        "value": "date",
        "index": 0,
    }
    amount_label = {
        "value": "amount",
        "index": 0,
    }

    def get_money_per_time(self):
        try:
            rows = self.__get_lines_of_file(self.file_path)
        except FileNotFoundError:
            print("No CSV file set!")
            exit(1)

        try:
            entries = self.__get_entries_per_date(rows)
        except ValueError:
            print("Date or amount label are not correct")
            exit(1)

        return self.__sum_total(entries)

    def __get_lines_of_file(self, file_path):
        with open(file_path, "r", encoding="utf-8-sig") as file:
            return file.readlines()

    def __get_row_columns(self, row):
        return row.split(",")

    def __set_index_of__specific_columns(self, columns):
        index = 0
        is_date_label_set = False
        is_amount_label_set = False

        for column in columns:
            column = column.lower()
            if column == self.date_label['value'].lower():
                is_date_label_set = True
                self.date_label['index'] = index
            elif column == self.amount_label['value'].lower():
                is_amount_label_set = True
                self.amount_label['index'] = index

            index += 1

        if not is_date_label_set or not is_amount_label_set:
            raise ValueError

    def __get_entries_per_date(self, rows):
        amount_per_date = {}

        execute_only_the_first_time = True
        for row in rows:
            columns = self.__get_row_columns(row)

            if execute_only_the_first_time:
                execute_only_the_first_time = False
                self.__set_index_of__specific_columns(columns)
                continue

            date = columns[self.date_label['index']]
            amount = columns[self.amount_label['index']]

            if date in amount_per_date:
                amount_per_date[date] += float(amount)
            else:
                amount_per_date[date] = float(amount)

        return self.__sort_by_date_keys(amount_per_date)

    def __sort_by_date_keys(self, dictionary):
        return dict(
            sorted(
                dictionary.items(),
                key=lambda x: datetime.strptime(x[0], self.date_format))
        )

    def __sum_total(self, entries):
        total = 0
        for date, amount in entries.items():
            total += amount
            entries[date] = total

        return entries


if __name__ == "__main__":
    money = MoneyOverTime()
    money_per_time = money.get_money_per_time()

    plt.plot(money_per_time.keys(), money_per_time.values())
    plt.show()
