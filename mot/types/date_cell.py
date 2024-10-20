DEFAULT_DATE_LABEL = "date"
DEFAULT_DATE_FORMAT = "%d/%m/%Y"

class DateCell:
    def __init__(self, label: str = DEFAULT_DATE_LABEL, date_format: str = DEFAULT_DATE_FORMAT):
        self.label = label
        self.date_format = date_format
