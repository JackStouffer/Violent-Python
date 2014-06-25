#!/usr/bin/python


def escape_color(string, color, bold):
    attr = []

    # a hacked switch statement
    color_code = {
        "green": "32",
        "red": "31",
        "yellow": "33",
        "blue": "34",
        "pink": "35",
        "grey": "30"
    }.get(color, '37')

    attr.append(color_code)

    if bold:
        attr.append('1')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
