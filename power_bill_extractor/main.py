import csv
import os

import click
from bill import PowerBill


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


if __name__ == "__main__":
    # touch()
    main()
