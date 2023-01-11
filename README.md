# Power Bill Extractor

Power Bill Extractor will take a PDF of a Florida Power and Light (FPL) bill, extract power usage and costs, and output it to a CSV file.

## Description

I created this project to better help track my home power usage and costs. FPL's website will only save the last two years of billing. This means I could not compare usage and data through their site over long term. I started saving the bills in PDF format, but wasn't able to compare them easily. *Enter the Power Bill Extractor.* It pulls the information I want to compare from each bill, and exports it to a CSV file for later use.

This is a project primarily developed for personal use to gather the described information. As such, it will only successfully pull the data from the FPL bills as provided. It has not been tested or developed for PDFs provided from other companies.

While working on this project I tried several different PDF parsing libraries. I ended up settling with `pdfminer.six` because of it's better use of grouping relevant blocks of text together. It refers to these groupings as text boxes, and I simply refer to them as boxes in the code for this project. Given that it does a better job of creating these boxes, it makes it easier for Power Bill Extractor to then pull the correct information. Many other libraries only really had basic text extraction, and would leave the data as one long difficult string to parse.

## Features

- All code written in Python 3.
- Power Bill Extractor will only take PDF files formatted in the specific way that FPL produces them.
- Parse all relevant data a from FPL bill and output it to a new or existing CSV file.
- Can gather info from all bills in a single folder.

#### Information pulled from the bill include:

- Total amount owed for the bill.
- Start date of billing period.
- End date of billing period.
- Service length (days) of the bill.
- Current power meter reading.
- Previous power meter reading.
- Total kWh used for billing period.
- Non-fuel costs:
  - First 1000 kWh cost per kWh.
  - Over 1000 kWh cost per kWh.
- Fuel costs:
  - First 1000 kWh cost per kWh.
  - Over 1000 kWh cost per kWh.

## Getting Started

TODO

## Dependencies

- TODO

## Future

Future additions to the project may include:

- Add command line argument support.
  - Use of argparse.
  - Have optional argument to run a single file.
  - Have optional argument to run a specific directory.
- User input for file or directory if no arguments used.
- Only updating CSV from new files in given directory.
- Add other export options besides CSV.
- Add more error checking for file and directory opening.
- Option to display data in tables in terminal like `tabulate`.
