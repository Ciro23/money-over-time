from typing import Optional


class DiffOverTime:
    def __init__(
            self,
            source_file_path: str,
            reference_file_path: str,
            source_account: str,
            source_separator: Optional[str] = ",",
            source_date_format: Optional[str] = "%d/%m/%Y",
            source_date_label: Optional[str] = "date",
            source_amount_label: Optional[str] = "amount",
            reference_separator: Optional[str] = ",",
            reference_date_format: Optional[str] = "%d/%m/%Y",
            reference_date_label: Optional[str] = "date",
            reference_amount_label: Optional[str] = "amount",
    ):
        self.source_file_path = source_file_path
        self.source_separator = source_separator if source_separator is not None else ","
        self.account = source_account
        self.source_date = {
            "label": source_date_label if source_date_label is not None else "date",
            "format": source_date_format if source_date_format is not None else "%d/%m/%Y",
            "index": -1,
        }
        self.source_amount = {
            "label": source_amount_label if source_amount_label is not None else "amount",
            "index": -1,
        }

        self.reference_file_path = reference_file_path
        self.reference_separator = reference_separator
        self.reference_date = {
            "label": reference_date_label if reference_date_label is not None else "date",
            "format": reference_date_format if reference_date_format is not None else "%d/%m/%Y",
            "index": -1,
        }
        self.reference_amount = {
            "label": reference_amount_label if reference_amount_label is not None else "amount",
            "index": -1,
        }

    def get_diff_over_time(self):
        pass