from datetime import datetime


class MoneyOverTime:
    file_path = ""
    date_format = "%d/%m/%Y"
    date_label = {
        "value": "date",
        "index": None,
    }
    amount_label = {
        "value": "amount",
        "index": None,
    }
    separator = ","

    def __init__(
        self,
        file_path,
        separator,
        date_format,
        date_label,
        amount_label,
    ):
        self.file_path = file_path

        if date_format is not None:
            self.date_format = date_format

        if date_label is not None:
            self.date_label['value'] = date_label

        if amount_label is not None:
            self.amount_label['value'] = amount_label

        if separator is not None:
            self.separator = separator

    def get_money_per_time(self):
        try:
            rows = self.__get_lines_of_file()
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        try:
            entries = self.__get_entries_per_date(rows)
        except ValueError as e:
            raise ValueError(e)

        return self.__sum_total(entries)

    def __get_lines_of_file(self):
        with open(self.file_path, "r", encoding="utf-8-sig") as file:
            return file.read().splitlines()

    def __get_row_columns(self, row):
        return row.split(self.separator)

    def __set_index_of_specific_columns(self, columns):
        index = 0

        for column in columns:
            column = column.lower()
            if column == self.date_label['value'].lower():
                self.date_label['index'] = index
            elif column == self.amount_label['value'].lower():
                self.amount_label['index'] = index

            index += 1

        if self.date_label['index'] is None or self.amount_label['index'] is None:
            raise ValueError

    def __get_entries_per_date(self, rows):
        amount_per_date = {}

        execute_only_the_first_time = True
        for row in rows:
            columns = self.__get_row_columns(row)

            if execute_only_the_first_time:
                execute_only_the_first_time = False
                try:
                    self.__set_index_of_specific_columns(columns)
                except ValueError as e:
                    raise ValueError(e)
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
