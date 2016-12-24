#!/usr/bin/env python
#
# Filename:     github-admin-toolkit.py
#
# Description:  Helper module that handles JSON parsing and
#               data processing for the github-admin-toolkit
#

import os
import requests
import sys
import urllib2

debug = None        # Debug mode flag
py3 = False         # Detect python version

def main():

    # Check if DEBUG mode is set
    global debug
    if os.environ.get('DEBUG'):
        debug = True
        print "(debug) " + sys.argv[0] + ": In debug mode"
        
    # Get python interpreter version
    py3 = getPythonVersion() > 2
    
    
    if debug:
        
        print "(debug) " + sys.argv[0] + ": Python version " + str(getPythonVersion())
        
        if os.environ.get('APIBASE'):
            print "(debug) " + sys.argv[0] + ": APIBASE set to '" + os.environ['APIBASE'] + "'"
        if os.environ.get('SERVER'):
            print "(debug) " + sys.argv[0] + ": SERVER set to '" + os.environ['SERVER'] + "'"
        if os.environ.get('OWNER'):
            print "(debug) " + sys.argv[0] + ": OWNER set to '" + os.environ['OWNER'] + "'"
        if os.environ.get('REPO'):
            print "(debug) " + sys.argv[0] + ": REPO set to '" + os.environ['REPO'] + "'"
        if os.environ.get('AUTH'):
            print "(debug) " + sys.argv[0] + ": AUTH set to '" + os.environ['AUTH'] + "'"
        if os.environ.get('SCRIPTNAME'):
            print "(debug) " + sys.argv[0] + ": SCRIPTNAME set to '" + os.environ['SCRIPTNAME'] + "'"
        if len(sys.argv) > 0:
            print "(debug) " + sys.argv[0] + ": Argument list is '" + str(sys.argv) + "'"
        
        print " "
    
    # The first argument should be the name of the method we will use. Use the dictionary to call the correct method
    if len(sys.argv) > 0:
        getattr(sys.modules[__name__], str(sys.argv[1]))()        
    else:
        print "ERROR (" + sys.argv[0] + "): We need the method to run passed in as the first argument."
        _exit(1)
    

#end main()-------------------------------

def getCollaborators():

    # We should know which interpreter we are using
    global py3

    print getScriptName() + ": Fetching..."
    
    # Get Required vars
    owner = getOwner()
    auth = getAuth()
    
    # Check if OWNER exists on the GitHub server
    
    # Check if REPO provided. If not, iterate over all repos. 

#end get-collaborators()-------------------------------

def getPythonVersion():
    
    return sys.version_info[0]

#end getPythonVersion()-------------------------------

def getServer():
    
    # Get the value for the SERVER
    
    if os.environ.get('SERVER'):
        return str(os.environ['SERVER'])
    
    else:
        
        userInput = "Enter the name of the GitHub SERVER and press [ENTER]: "
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getServer()-------------------------------

def getOwner():
    
    # Get the value for the OWNER
    
    if os.environ.get('OWNER'):
        return str(os.environ['OWNER'])
    
    else:
        
        userInput = "Enter the name of the GitHub OWNER and press [ENTER]: "
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getOwner()-------------------------------

def getRepo():
    
    # Get the value for the REPO
    
    if os.environ.get('REPO'):
        return str(os.environ['REPO'])
    
    else:
        
        userInput = "Enter the name of the GitHub REPO and press [ENTER]: "
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getRepo()-------------------------------

def getAuth():
    
    # Get the value for the AUTH token
    
    if os.environ.get('AUTH'):
        return str(os.environ['AUTH'])
    
    else:
        
        print "Enter a GitHub Personal Access Token to authenticate with and press [ENTER]";
        print "(Note: A token for this server can be created at https://" + str(getServer()) + "/settings/tokens)";
        
        userInput = ": "
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))
        


#end getAuth()-------------------------------

def getScriptName():
    
    # Get the value for the SCRIPTNAME
    
    if os.environ.get('SCRIPTNAME'):
        return str(os.environ['SCRIPTNAME'])
    
    else:
        print "ERROR (" + sys.argv[0] + "): The SCRIPTNAME could not properly be determined!"
        _exit(1)

#end getServer()-------------------------------

def _exit(code):

    """ Performs proper clean up before exiting
    """
    log('Exit code = ' + str(code), logging.INFO)
    sys.exit(code)

#end _exit()-------------------------------

if __name__ == "__main__":
    main()
