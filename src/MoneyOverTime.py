from datetime import datetime


class MoneyOverTime:
    file_path = ""
    date_format = ""
    date_label = {
        "value": "",
        "index": 0,
    }
    amount_label = {
        "value": "",
        "index": 0,
    }

    def __init__(self, file_path, date_format, date_label, amount_label):
        self.file_path = file_path

        if date_format is None:
            date_format = "%d/%m/%Y"
        self.date_format = date_format

        if date_label is None:
            date_label = "date"
        self.date_label['value'] = date_label

        if amount_label is None:
            amount_label = "amount"
        self.amount_label['value'] = amount_label

    def get_money_per_time(self):
        rows = self.__get_lines_of_file(self.file_path)
        entries = self.__get_entries_per_date(rows)

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
