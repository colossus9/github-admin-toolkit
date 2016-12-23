#!/usr/bin/env python
#
# Filename:     get-collaborators.py
#
# Description:  Helper module that handles JSON parsing and
#               data processing for the get-collaborators script
#

import os
import requests
import urllib2

def main():

    print "Inside get-collaborators.py"
    print "APIBASE is '" + os.environ['APIBASE'] + "'"
    #json.load(urllib2.urlopen("url"))

#end main()-------------------------------

def _exit(code):

    """ Performs proper clean up before exiting the program
    """
    log('Exit code = ' + str(code), logging.INFO)
    sys.exit(code)

#end _exit()-------------------------------

if __name__ == "__main__":
    main()
