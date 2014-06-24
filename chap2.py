#!/usr/bin/python

import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)


def connect_scan(host, port):
    try:
        connect = socket(AF_INET, SOCK_STREAM)
        connect.connect((host, port))

        connect.send('test\r\n')
        result = connect.recv(100)

        screenLock.acquire()
        print '%d/tcp open' % port
        print "Results: " + str(result) + "\n"
    except:
        screenLock.acquire()
        print 'port %d is closed\n' % port
    finally:
        connect.close()
        screenLock.release()


def port_scan(host, ports):
    try:
        ip = gethostbyname(host)
    except:
        print 'could not find a ip for the host'
        return

    try:
        name = gethostbyaddr(ip)
        print 'Scan results for: ' + name[0]
    except:
        print 'Scan results for: ' + ip

    setdefaulttimeout(1)

    for port in ports:
        t = Thread(target=connect_scan, args=(host, int(port)))
        t.start()


def main():
    parser = optparse.OptionParser('usage: chap2.py -H' +
                                   ' <target_host> -p <target_port>')
    parser.add_option('-H', dest='host', type='string', help='target host')
    parser.add_option('-p',
                      dest='port',
                      type='string',
                      help='target ports seperated by commas')

    (options, args) = parser.parse_args()

    host = options.host
    port = str(options.port).split(',')

    if not host or not port:
        print parser.usage
        exit(0)

    port_scan(host, port)

if __name__ == '__main__':
    main()
