from MoneyOverTime import MoneyOverTime
import matplotlib.pyplot as plt
import argparse


class Main:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.add_arguments()
        self.args = self.parser.parse_args()

    def add_arguments(self):
        self.parser.add_argument(
            "--file",
            type=str,
            help="CSV containing all transactions path"
        )
        self.parser.add_argument(
            "--separator",
            type=str,
            nargs="?",
            help="Column separator, default \",\""
        )
        self.parser.add_argument(
            "--date_format",
            type=str,
            nargs="?",
            help="Date format used in the CSV file, default \"%%d/%%m/%%Y\""
        )
        self.parser.add_argument(
            "--date_label",
            type=str,
            nargs="?",
            help="Date label used in the CSV file, default \"date\""
        )
        self.parser.add_argument(
            "--amount_label",
            type=str,
            nargs="?",
            help="Amount label used in the CSV file, default \"amount\""
        )

    def execute_program(self):
        money = MoneyOverTime(
            self.args.file,
            self.args.separator,
            self.args.date_format,
            self.args.date_label,
            self.args.amount_label,
        )

        try:
            money_per_time = money.get_money_per_time()
        except FileNotFoundError:
            print("File not found!")
            return
        except ValueError as e:
            print("Error reading the file, check if parameters are correct, use --help for more.", e)
            return

        plt.plot(money_per_time.keys(), money_per_time.values())
        plt.xticks(rotation = 45)
        plt.gca().set_xticks(plt.gca().get_xticks()[::30])
        plt.show()


if __name__ == "__main__":
    main = Main()
    main.execute_program()
