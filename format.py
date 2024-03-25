import textwrap
from Constants import STANDARD_TEXT_WIDTH, COLUMN_WIDTH



def format_textwrap(text: str) -> None:
    """
    format_textwrap() takes the given text and
    restricts the text to a standard text width.
    Then the text is printed to stdout.

    Paramters:
    text: string (The text to format)

    Returns:
    None
    """
    for line in textwrap.wrap(text, width=STANDARD_TEXT_WIDTH):
        print(line.strip())

def format_column(column: str) -> str:
    """
    format_column() takes the given column
    string and attempts to center the column
    to a standard width. Returns the centered
    column string.

    Paramters:
    column: string (The column of text to center)

    Returns:
    str(column).center(COLUMN_WIDTH, ' '): str (The centered version of the passed in column string)
    """
    return str(column).center(COLUMN_WIDTH, ' ')

def format_divider() -> str:
    """
    format_divider() returns the string
    comprised of repeating `-` matching
    the length of the standard text width.

    Paramters:
    None

    Returns:
    "-" * STANDARD_TEXT_WIDTH: str (A string comprised of standard text width `-`s)
    """
    return "-" * STANDARD_TEXT_WIDTH

def format_welcome_text(text: str) -> str:
    """
    format_welcome_text() returns the
    string centered to a standard text
    width offest by two characters.

    Paramters:
    text: string (The text to format)

    Returns:
    f"|{str(text).center(STANDARD_TEXT_WIDTH - 2, ' ')}|": string (The given text centered to a width of standard text width)
    """
    return f"|{str(text).center(STANDARD_TEXT_WIDTH - 2, ' ')}|"

def format_escape_single_and_double_quotes(text: str) -> str:
    """
    format_escape_single_and_double_quotes() returns
    the given string with all single and double quotes
    escaped.

    Paramters:
    text: string (The text containing single and/or double quotes to escape)

    Returns:
    text.replace("\'", "\\\'").replace("\"", "\\\""): string (The given text with all single and/or double quotes escaped)
    """
    return text.replace("\'", "\\\'").replace("\"", "\\\"")