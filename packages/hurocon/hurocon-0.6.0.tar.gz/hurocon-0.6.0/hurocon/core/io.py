""" Input/Output wrappers """
import textwrap


def printx(*text, limit_line_length: bool = False):
    """
    Enhanced long-text printing function

    :param limit_line_length: Split line by length, defaults to False
    """
    final_text = ''
    for line in text:
        line_processed = str(line)
        final_text += prettify(line_processed) if limit_line_length else line_processed

    print(final_text)


def prettify(text) -> str:
    """
    Prettify the text

    Features:
    - Split text by length

    :param text: Text to process
    :return: Formatted string, ready for printing
    """
    return textwrap.fill(
        text,
        width=80,
        tabsize=4,
        replace_whitespace=False
    )
