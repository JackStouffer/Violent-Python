#!./env/bin/python

import nmap
import socket
import optparse

from utilities import escape_color


def nmap_scan(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    ip = socket.gethostbyaddr(host)[-1][0]
    state = scanner[ip]['tcp'][int(port)]['state']
    
    if state == "open":
        print escape_color(" [*] " + host + " tcp/" + port + " " + state, "green")
    else:
        print escape_color(" [*] " + host + " tcp/" + port + " " + state, "red")


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
