Jack's Super Awesome Security Toolkit for Attractive People
===========================================================

**Don't be a moron, please don't use this for something illegal.**

This is code that I am writing by following the "Violent Python: A Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers" book. The code is not an exact copy because most of the code in the book is very un-pythonic, but they perform roughly the same tasks.

Install the required packages:

    pip install -r requirements.txt

Included Programs
-----------------

Individual usage can be found by typing "./programname.py --help"

###ftp.py

Scan hosts for anonymous logins or brute force the password for a user.

###nmap_scan.py

Scan the ports on the provided host

###ssh_botnet.py

Simple script to control multiple ssh hosts at once provided you have the user names and passwords, which you can get from:

###ssh\_brute\_forcer.py

Brute forces a host's ssh server with a provided worldlist

###url_checker.py

Find hidden paths on a http sever

License
-------

All code here is under the MIT license.
