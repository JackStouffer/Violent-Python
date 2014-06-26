#!./env/bin/python

""" Port Scanner

    This program scans the designated ports on a the specified host using
    nmap.

    Usage:
        nmap_scan.py <host> <ports>
        nmap_scan.py -h | --help
        nmap_scan.py --version

    Options:
        password_file   File to read wordlist/url patterns from
        url             Url to run against
        -h, --help      Display this message
        --version       Display the version of this program
        -a, --async     Send requests asynchronously (faster but straining on server)

    Examples:
        ./nmap_scan.py localhost 21,22,80,443
"""

import nmap
import socket

from docopt import docopt
from utilities import escape_color


def nmap_scan(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    ip = socket.gethostbyaddr(host)[-1][0]
    state = scanner[ip]['tcp'][int(port)]['state']

    if state == "open":
        print escape_color(" [*] " + host + " tcp/" + port + " " + state, "green")
    elif state == "filtered":
        print escape_color(" [*] " + host + " tcp/" + port + " " + state, "pink")
    else:
        print escape_color(" [*] " + host + " tcp/" + port + " " + state, "red")


def main(host, ports):
    for port in ports:
        nmap_scan(host, port)

if __name__ == '__main__':
    arguments = docopt(__doc__, version=0.1)

    host = arguments['<host>']
    ports = arguments['<ports>'].split(',')
    main(host, ports)
