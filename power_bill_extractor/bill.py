import click
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal

# Test commit
x = 1
y = 2

if x + y == 3:
    click.echo(click.style("Yay it works!", fg="green"))
