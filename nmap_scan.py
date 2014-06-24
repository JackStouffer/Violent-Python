#!/usr/bin/python

import sys
import nmap
import socket
import optparse


def escape_color(string, status, bold):
    attr = []
    if status:
        # green
        attr.append('32')
    else:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def nmap_scan(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    ip = socket.gethostbyaddr(host)[-1][0]
    state = scanner[ip]['tcp'][int(port)]['state']
    if sys.stdout.isatty():
        if state == "open":
            print escape_color(" [*] " + host + " tcp/" + port + " " + state, True, False)
        else:
            print escape_color(" [*] " + host + " tcp/" + port + " " + state, False, False)
    else:
        print " [*] " + host + " tcp/" + port + " " + state


def main():
    parser = optparse.OptionParser('usage%prog '
                                   '-H <target host name> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',
                      help='specify target port[s] separated by comma')

    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')

    if (tgtHost is None) or (tgtPorts[0] is None):
        print parser.usage
        exit(0)

    for tgtPort in tgtPorts:
        nmap_scan(tgtHost, tgtPort)

if __name__ == '__main__':
    main()
