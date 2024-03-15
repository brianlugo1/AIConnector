import textwrap
from Constants import STANDARD_TEXT_WIDTH, COLUMN_WIDTH



def format_textwrap(text):
    for line in textwrap.wrap(text, width=STANDARD_TEXT_WIDTH):
        print(line.strip())

def format_column(column):
    return str(column).center(COLUMN_WIDTH, ' ')

def format_divider():
    return "-" * STANDARD_TEXT_WIDTH

def format_welcome_text(text):
    return f"|{str(text).center(STANDARD_TEXT_WIDTH - 2, ' ')}|"

def format_escape_single_and_double_quotes(text):
    return text.replace("\'", "\\\'").replace("\"", "\\\"")