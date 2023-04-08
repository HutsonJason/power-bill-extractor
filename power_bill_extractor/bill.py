import datetime
import re
from dataclasses import dataclass, field

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


@dataclass
class PowerBill:
    pdf_file: str

    boxes: list[str] = field(init=False)
    start_date: datetime.date = field(init=False)
    end_date: datetime.date = field(init=False)
    service_length: int = field(init=False)
    bill_amount: float = field(init=False)
    current_meter_reading: int = field(init=False)
    previous_meter_reading: int = field(init=False)
    kwh_used: int = field(init=False)
    nonfuel_first_1000: float = field(init=False)
    nonfuel_over_1000: float = field(init=False)
    fuel_first_1000: float = field(init=False)
    fuel_over_1000: float = field(init=False)

    def __post_init__(self) -> None:
        """Gets a list of 'text boxes' from pdfminer that are groups of text."""
        self.boxes = [
            element.get_text()
            for page in extract_pages(self.pdf_file)
            for element in page
            if isinstance(element, LTTextBoxHorizontal)
        ]

        for i, box in enumerate(self.boxes):
            """Gets the start date, end date, and service length of the bill.
            Example regex search:
                'For: Jan 26, 2022 to Feb 25, 2022 (30 days)'"""
            if matches := re.search(
                r"For: ([a-z]{3} [0-9]{2}, 20[0-9]{2}) to ([a-z]{3} [0-9]{2}, 20[0-9]{2}) \(([0-9]{2}) days\)",
                box,
                re.IGNORECASE,
            ):
                # Set the groups to the variables.
                _start_date, _end_date, _service_length = matches.groups()
                # Set the date format used in the PDF.
                date_format = "%b %d, %Y"
                # Format the dates and days.
                self.start_date = datetime.datetime.strptime(
                    _start_date, date_format
                ).date()
                self.end_date = datetime.datetime.strptime(
                    _end_date, date_format
                ).date()
                self.service_length = int(_service_length)

            """Gets the total amount owed for the bill."""
            # The total bill is in the index between current bill and total amount you owe.
            if (
                "current bill" in box.lower()
                and "total amount you owe" in self.boxes[i + 2].lower()
            ):
                self.bill_amount = float(self.boxes[i + 1].strip().removeprefix("$"))

            """Gets the current meter reading for the bill."""
            if matches := re.search(r"current\n(\d{5})", box, re.IGNORECASE):
                self.current_meter_reading = int(matches.group(1))

            """Gets the previous meter reading for the bill. """
            if matches := re.search(r"previous\n(\d{5})", box, re.IGNORECASE):
                self.previous_meter_reading = int(matches.group(1))

            """Gets the non-fuel costs for the bill."""
            if "Non-fuel:" in box:
                if matches := re.search(
                    r"First 1000 kWh at \$(0\.\d+)\)\n\(Over 1000 kWh at \$(0\.\d+)",
                    self.boxes[i + 1],
                    re.IGNORECASE,
                ):
                    self.nonfuel_first_1000 = float(matches.group(1))
                    self.nonfuel_over_1000 = float(matches.group(2))

            """Gets the fuel costs for the bill."""
            if "Fuel:" in box:
                if matches := re.search(
                    r"First 1000 kWh at \$(0\.\d+)\)\n\(Over 1000 kWh at \$(0\.\d+)",
                    self.boxes[i + 1],
                    re.IGNORECASE,
                ):
                    self.fuel_first_1000 = float(matches.group(1))
                    self.fuel_over_1000 = float(matches.group(2))

        """Gets kWh used"""
        self.kwh_used = self.current_meter_reading - self.previous_meter_reading
