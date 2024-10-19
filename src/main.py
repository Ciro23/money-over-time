from src.diff_over_time import get_diff_over_time, print_differences
from src.money_over_time import get_money_over_time, show_graph
from src.types.cell import Cell
from src.types.date_cell import DateCell, DEFAULT_DATE_LABEL, DEFAULT_DATE_FORMAT
from src.program_arguments import parse_program_arguments


class Main:

    def __init__(self):
        self.args = parse_program_arguments()

    def execute_program(self) -> None:
        result = True
        if self.args.command == "plot":
            result = self.__execute_money_over_time()
        elif self.args.command == "diff":
            result = self.__execute_diff_over_time()

        if result:
            exit(0)
        else:
            exit(1)

    def __execute_money_over_time(self) -> bool:
        date_cell = DateCell(
            DEFAULT_DATE_LABEL if self.args.date_label is None else self.args.date_label,
            DEFAULT_DATE_FORMAT if self.args.date_format is None else self.args.date_format
        )

        if self.args.exclude_label is None or self.args.exclude_value is None:
            excluding_cell = None
        else:
            excluding_cell = Cell(
                self.args.exclude_label,
                self.args.exclude_value
            )

        try:
            movements = get_money_over_time(
                self.args.file,
                self.args.delimiter,
                date_cell,
                self.args.amount_label,
                excluding_cell
            )
        except FileNotFoundError:
            print("File not found!")
            return False
        except ValueError as e:
            message = "Error reading the file, check if arguments are correct, use --help for more."
            if self.args.verbose:
                print(message, e)
            else:
                print(message)
            return False

        show_graph(movements, date_cell.date_format)
        return True

    def __execute_diff_over_time(self) -> bool:
        source_date_cell = DateCell(
            DEFAULT_DATE_LABEL if self.args.source_date_label is None else self.args.source_date_label,
            DEFAULT_DATE_FORMAT if self.args.source_date_format is None else self.args.source_date_format
        )
        reference_date_cell = DateCell(
            DEFAULT_DATE_LABEL if self.args.reference_date_label is None else self.args.reference_date_label,
            DEFAULT_DATE_FORMAT if self.args.reference_date_format is None else self.args.reference_date_format
        )

        if self.args.include_label is None or self.args.include_value is None:
            including_cell = None
        else:
            including_cell = Cell(
                self.args.include_label,
                self.args.include_value
            )

        try:
            differences_over_time = get_diff_over_time(
                self.args.source_file,
                self.args.reference_file,
                self.args.source_delimiter,
                including_cell,
                source_date_cell,
                self.args.source_amount_label,
                self.args.reference_delimiter,
                reference_date_cell,
                self.args.reference_amount_label
            )
        except FileNotFoundError as e:
            message = "File not found!"
            if self.args.verbose:
                print(message, e)
            else:
                print(message)
            return False
        except ValueError as e:
            message = "Error reading the files, check if arguments are correct, use --help for more."
            if self.args.verbose:
                print(message, e)
            else:
                print(message)
            return True

        print_differences(differences_over_time)
        return True


if __name__ == "__main__":
    main = Main()
    main.execute_program()
