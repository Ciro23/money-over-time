from datetime import datetime


class MoneyOverTime:
    file_path: str = ""
    date: dict = {
        "label": "date",
        "format": "%d/%m/%Y",
        "index": -1,
    }
    amount_label: dict = {
        "value": "amount",
        "index": -1,
    }
    separator: str = ","

    """
    It's possible to filter out some movements based on
    the value of a specifiable column.
    """
    skip_label: dict = {
        "value": "",
        "index": -1,
        "match": "",  # All movements matching this string are filtered out.
    }

    def __init__(
            self,
            file_path,
            separator,
            date_format,
            date_label,
            amount_label,
            skip_label,
            skip_value,
    ):
        self.file_path = file_path

        if date_format is not None:
            self.date['format'] = date_format

        if date_label is not None:
            self.date['label'] = date_label

        if amount_label is not None:
            self.amount_label['value'] = amount_label

        if separator is not None:
            self.separator = separator

        if skip_label is not None:
            self.skip_label['value'] = skip_label

        if skip_value is not None:
            self.skip_label['match'] = skip_value

    """
    Reads all the movements in the specified file and returns a dict
    with the date of the movement as the key and the sum of the amount
    of all movements, for that day, as the value.
    """
    def get_money_per_time(self) -> dict:
        try:
            rows: list = self.__get_lines_of_file()
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        try:
            entries: dict = self.__get_entries_per_date(rows)
        except ValueError as e:
            raise ValueError(e)

        return self.__sum_total(entries)

    def __get_lines_of_file(self) -> list:
        with open(self.file_path, "r", encoding="utf-8-sig") as file:
            return file.read().splitlines()

    def __get_row_columns(self, row: str) -> list:
        return row.split(self.separator)

    """
    It's necessary to retrieve the index of the "amount" and "date"
    columns from their label. This method is case-insensitive.
    """

    def __set_index_of_specific_columns(self, columns: list) -> None:
        index = 0

        for column in columns:
            column = column.lower()
            if column == self.date['label'].lower():
                self.date['index'] = index
            elif column == self.amount_label['value'].lower():
                self.amount_label['index'] = index
            elif column == self.skip_label['value'].lower():
                self.skip_label['index'] = index

            index += 1

        if self.date['index'] < 0 or self.amount_label['index'] < 0:
            raise ValueError("Could not find the index of the 'date' or 'amount' labels."
                             " Check if their specified label name match the ones in the csv file.")

    def __get_entries_per_date(self, rows: list) -> dict:
        amount_per_date: dict = {}
        execute_only_the_first_time: bool = True

        for row in rows:
            columns = self.__get_row_columns(row)

            if execute_only_the_first_time:
                execute_only_the_first_time = False
                try:
                    self.__set_index_of_specific_columns(columns)
                except ValueError as e:
                    raise ValueError(e)
                continue

            # If the index of the "column to skip" has been set,
            # then the value in the cell of this row must be checked,
            # so that it's skipped if there's a match.
            if self.skip_label['index'] >= 0:
                skip: str = columns[self.skip_label['index']]
                if skip.lower() == self.skip_label['match'].lower():
                    continue

            date = columns[self.date['index']]
            amount = columns[self.amount_label['index']]

            if date in amount_per_date:
                amount_per_date[date] += float(amount)
            else:
                amount_per_date[date] = float(amount)

        return self.__sort_by_date_keys(amount_per_date)

    """
    All movements must be sorted chronologically by the
    date they were made.
    """

    def __sort_by_date_keys(self, dictionary: dict) -> dict:
        return dict(
            sorted(
                dictionary.items(),
                key=lambda x: datetime.strptime(x[0], self.date['format'])
            )
        )

    """
    Given all movement entries, all the dates are grouped
    together as keys and the amount of each one is summed
    as the value.
    """

    def __sum_total(self, entries: dict) -> dict:
        total = 0
        for date, amount in entries.items():
            total += amount
            entries[date] = total

        return entries
