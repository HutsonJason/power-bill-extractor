import csv
import datetime
import os
import re

import click
from bill import PowerBill
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


@click.command()
@click.option(
    "-f",
    "--filename",
    type=click.Path(exists=True),
    prompt="Enter directory of power bills",
)
@click.option("-o", "--output", type=click.Path())
def main(filename, output):
    if output is None:
        output = f"{filename}\\bills.csv"
    else:
        output = f"{filename}\\{output}"
    file_directory = filename
    file_list = get_file_list(file_directory)
    write_header = not os.path.exists(output)

    # Write and save CSV file.
    with open(output, "a", newline="") as csv_file:
        fieldnames = [
            "Start Date",
            "End Date",
            "Service Length",
            "Bill Amount",
            "Current Meter Reading",
            "Previous Meter Reading",
            "kWh Used",
            "Non-fuel First 1000 kWh",
            "Non-fuel Over 1000 kWh",
            "Fuel First 1000 kWh",
            "Fuel Over 1000 kWh",
        ]
        # Set dictionary writer and write header if new file.
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        # Add row for every PDF file.
        for file in file_list:
            pdf_file = f"{file_directory}/{file}"
            power_bill = PowerBill(pdf_file)
            # boxes = get_boxes(pdf_file)
            # start_date, end_date, service_length = get_dates(boxes)
            # total_amount_owed = get_bill_amount(boxes)
            # current_meter_reading = get_current_reading(boxes)
            # previous_meter_reading = get_previous_reading(boxes)
            # kwh_used = current_meter_reading - previous_meter_reading
            # nonfuel_first_1000, nonfuel_over_1000 = get_nonfuel_costs(boxes)
            # fuel_first_1000, fuel_over_1000 = get_fuel_costs(boxes)

            writer.writerow(
                {
                    "Start Date": power_bill.start_date,
                    "End Date": power_bill.end_date,
                    "Service Length": power_bill.service_length,
                    "Bill Amount": power_bill.bill_amount,
                    "Current Meter Reading": power_bill.current_meter_reading,
                    "Previous Meter Reading": power_bill.previous_meter_reading,
                    "kWh Used": power_bill.kwh_used,
                    "Non-fuel First 1000 kWh": power_bill.nonfuel_first_1000,
                    "Non-fuel Over 1000 kWh": power_bill.nonfuel_over_1000,
                    "Fuel First 1000 kWh": power_bill.fuel_first_1000,
                    "Fuel Over 1000 kWh": power_bill.fuel_over_1000,
                }
            )


def get_file_list(directory: str) -> list[str]:
    """Gets a sorted list of PDF files from the provided path.

    Retrieves a list of all PDF files from the given directory. First it checks every
    file for correct .pdf extension, then adds the file name to the list. Finally, It
    will sort them, then return a list of filenames as a string.

    Args:
        directory: The directory of the PDF files to retrieve.

    Returns:
        A sorted list of PDF files in the given directory.
    """
    file_list = [file for file in os.listdir(directory) if file.endswith(".pdf")]
    return sorted(file_list)


def get_boxes(pdf_file: str) -> list[str]:
    """Gets a list of 'text boxes' from pdfminer that are groups of text.

    Retrieves groups of text that pdfminer determines are part of a text box from the
    given PDF file. It will iterate through each page of the PDF, then what pdfminer
    determines is an element of each page. If the element is a text box, it's added
    to the boxes list.

    Args:
        pdf_file: The string value of the PDF file to parse.

    Returns:
        A list of strings of all groups, or text boxes, of the PDF file.
    """
    boxes = [
        element.get_text()
        for page in extract_pages(pdf_file)
        for element in page
        if isinstance(element, LTTextBoxHorizontal)
    ]
    return boxes


def get_dates(boxes: list[str]) -> tuple:
    """Gets the start date, end date, and service length of the bill.

    Iterates through the boxes list to find the start date, end date, and service length
    of the bill. Dates are converted to a datetime format.
    Example regex search:
        'For: Jan 26, 2022 to Feb 25, 2022 (30 days)'

    Args:
        boxes: A list of strings with the groups, or 'boxes' of text from the PDF.

    Returns:
        A tuple of the start date (datetime.date), end date (datetime.date), and
        service length (int).
    """
    for box in boxes:
        if matches := re.search(
            r"For: ([a-z]{3} [0-9]{2}, 20[0-9]{2}) to ([a-z]{3} [0-9]{2}, 20[0-9]{2}) \(([0-9]{2}) days\)",
            box,
            re.IGNORECASE,
        ):
            # Set the groups to the variables.
            start_date, end_date, service_length = matches.groups()
            # Set the date format used in the PDF.
            date_format = "%b %d, %Y"
            # Format the dates and days.
            start_date = datetime.datetime.strptime(start_date, date_format).date()
            end_date = datetime.datetime.strptime(end_date, date_format).date()
            service_length = int(service_length)
            return start_date, end_date, service_length


def get_bill_amount(boxes: list[str]) -> float:
    """Gets the total amount owed for the bill.

    Iterates through the boxes list to find the total amount owed for the bill. The
    amount owed is in the index between the 'current bill' and 'total amount you owe'.
    When those two matches are found, the amount owed is returned after formatting.

    Args:
        boxes: A list of strings with the groups, or 'boxes' of text from the PDF.

    Returns:
        A float of the total amount owed for the bill.
    """
    for i, box in enumerate(boxes):
        # The total bill is in the index between current bill and total amount you owe.
        if (
            "current bill" in box.lower()
            and "total amount you owe" in boxes[i + 2].lower()
        ):
            return float(boxes[i + 1].strip().removeprefix("$"))


def get_current_reading(boxes: list[str]) -> int:
    """Gets the current meter reading for the bill.

    Gets the current meter reading from the bill using a regex search. The string
    that the search is looking for in the boxes list is on 2 different lines.
    Example of the regex search:
        'Current
         25549'

    Args:
        boxes: A list of strings with the groups, or 'boxes' of text from the PDF.

    Returns:
        An int of the current meter reading.
    """
    for box in boxes:
        if matches := re.search(r"current\n(\d{5})", box, re.IGNORECASE):
            return int(matches.group(1))


def get_previous_reading(boxes: list[str]) -> int:
    """Gets the previous meter reading for the bill.

    Gets the previous meter reading from the bill using a regex search. The string
    that the search is looking for in the boxes list is on 2 different lines.
    Example of the regex search:
        'Previous
         24563'

    Args:
        boxes: A list of strings with the groups, or 'boxes' of text from the PDF.

    Returns:
        An int of the previous meter reading.
    """
    for box in boxes:
        if matches := re.search(r"previous\n(\d{5})", box, re.IGNORECASE):
            return int(matches.group(1))


def get_nonfuel_costs(boxes: list[str]) -> tuple:
    """Gets the non-fuel costs for the bill.

    Searches for the string in the boxes list with 'Non-fuel:'. Once it finds that,
    a regex search is done on the index after to extract both the first 1000 kWh cost,
    and over 1000 kWh cost. These are two different prices, but both in the same box.
    Example of the regex search:
        'First 1000 kWh at $0.073710)
         (Over 1000 kWh at $0.083710'

    Args:
        boxes: A list of strings with the groups, or 'boxes' of text from the PDF.

    Returns:
        A tuple of two floats with the first 1000 kWh cost, and over 1000 kWh cost.
    """
    for i, box in enumerate(boxes):
        if "Non-fuel:" in box:
            if matches := re.search(
                r"First 1000 kWh at \$(0\.\d+)\)\n\(Over 1000 kWh at \$(0\.\d+)",
                boxes[i + 1],
                re.IGNORECASE,
            ):
                return float(matches.group(1)), float(matches.group(2))


def get_fuel_costs(boxes: list[str]) -> tuple:
    """Gets the fuel costs for the bill.

    Searches for the string in the boxes list with 'Fuel:'. Once it finds that, a regex
    search is done on the index after to extract both the first 1000 kWh cost, and over
    1000 kWh cost. These are two different prices, but both in the same box.
    Example of the regex search:
        'First 1000 kWh at $0.034870)
         (Over 1000 kWh at $0.044870'

    Args:
        boxes: A list of strings with the groups, or 'boxes' of text from the PDF.

    Returns:
        A tuple of two floats with the first 1000 kWh cost, and over 1000 kWh cost.
    """
    for i, box in enumerate(boxes):
        if "Fuel:" in box:
            if matches := re.search(
                r"First 1000 kWh at \$(0\.\d+)\)\n\(Over 1000 kWh at \$(0\.\d+)",
                boxes[i + 1],
                re.IGNORECASE,
            ):
                return float(matches.group(1)), float(matches.group(2))


if __name__ == "__main__":
    # touch()
    main()
