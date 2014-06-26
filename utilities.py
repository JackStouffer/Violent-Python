#!/usr/bin/python

import sys


def escape_color(string, color, bold=False):
    """ Escape a string with the ansi code for the provided color in
        tty consoles.
    """

    attr = []

    # a hacked switch statement
    color_code = {
        "green": "32",
        "red": "31",
        "yellow": "33",
        "blue": "34",
        "pink": "35",
        "black": "30",
        "cyan": "36",
    }.get(color, '37')

    attr.append(color_code)

    if bold:
        attr.append('1')

    if sys.stdout.isatty():
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
    else:
        return string
