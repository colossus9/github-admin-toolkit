#!/usr/bin/env python
#
# Filename:     github-admin-toolkit.py
#
# Description:  Helper module that handles JSON parsing and
#               data processing for the github-admin-toolkit
#

import json
import os
import requests
import sys
import urllib2

debug           = None                              # Debug mode flag
py3             = False                             # Detect python version
httpHeaders     = {}                                # HTTP header value
acceptHeader    = "application/vnd.github.v3+json"  # Accept header for HTTP call
auth            = None                              # If needed, the Authorization token



"""

 +--------------------------------------------+
 |                                            |
 |  GitHub Admin Toolkit script logic         |
 |                                            |
 +--------------------------------------------+
 
"""



def getCollaborators():

    if getDebug():
        debugMsg('Entered getCollaborators()')
        
    # Check if OWNER exists on the GitHub server
    responseCode, responseJSON = getHTTPResponse('/orgs/' + getOwner())
    
    print (str(responseCode) + str(responseJSON))
    
    # Check if REPO provided. If not, iterate over all repos. 

#end get-collaborators()-------------------------------



"""

 +--------------------------------------------+
 |                                            |
 |  Helper methods                            |
 |                                            |
 +--------------------------------------------+
 
"""

def getHTTPResponse(path):
    
    global auth
    
    # Build the request object
    request = None
    url = getAPIBase() + path
    
    # Load appropriate HTTP libs
    try:
        from urllib.request import Request, urlopen, HTTPError, URLError     # Python 3
    except:
        from urllib2 import Request, urlopen, HTTPError, URLError            # Python 2
    
    request = Request(url)

    # Set needed header(s)
    request.add_header('Accept', getHTTPHeader('Accept'))
    
    # ...including Authentication header (if needed)
    if not auth == None:        
        if getDebug():
            debugMsg('Using Authentication Header')            
        request.add_header('Authorization', getHTTPHeader('Authorization'))
    
    # Get the response
    try:
        response = urlopen(request)
    except HTTPError as e:
        errMsg("HTTP Status Code is " + str(e.code) + ". Please check your inputs and try again.")
        _exit(1)
    else:
        # Return JSON object
        return response.code, json.loads(response.read())

#end getHTTPResponse()-------------------------------

def getPythonVersion():
    
    return sys.version_info[0]

#end getPythonVersion()-------------------------------

def getDebug():
    
    global debug
    return debug

#end getDebug()-------------------------------

def setDebug():
    
    global debug
    
    if os.environ.get('DEBUG'):
        debug = True

#end setDebug()-------------------------------

def debugMsg(msg):
    
    print "(debug) " + sys.argv[0] + ": " + msg
    
#end debugMsg()-------------------------------

def errMsg(msg):
    
    print "ERROR (" + sys.argv[0] + "): " + msg
    
#end debugMsg()-------------------------------

def getAPIBase():
    
    # Get the value for the APIBASE
    
    if os.environ.get('APIBASE'):
        return str(os.environ['APIBASE'])
    
    else:
        
        userInput = "Enter the API base url of the GitHub server (i.e. https://api.github.com) and press [ENTER]: "
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getAPIBase()-------------------------------

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

def getHTTPHeader(header):
    
    global httpHeaders
    global acceptHeader
    
    # Set the recommended Accept header
    httpHeaders['Accept'] = acceptHeader
    
    # Check if we are requesting an Authorization header
    if header == 'Authorization':
        httpHeaders[header] = "token " + getAuth()
    
    return httpHeaders[header]

#end getHTTPHeader()-------------------------------

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
    
    global auth
    
    if auth == None:
        setAuth()
    
    return auth

#end getRepo()-------------------------------

def setAuth():
    
    global auth
    
    # Get the value for the AUTH token
    
    if os.environ.get('AUTH'):
        auth = str(os.environ['AUTH'])
    
    else:
        
        print "Enter a GitHub Personal Access Token to authenticate with and press [ENTER]";
        print "(Note: A token for this server can be created at https://" + str(getServer()) + "/settings/tokens)";
        
        userInput = ": "
        token = ""
        
        if py3:
            auth = str(input(userInput))
        else:
            auth = str(raw_input(userInput))

#end setAuth()-------------------------------

def getScriptName():
    
    # Get the value for the SCRIPTNAME
    
    if os.environ.get('SCRIPTNAME'):
        return str(os.environ['SCRIPTNAME'])
    
    else:
        errMsg("The SCRIPTNAME could not properly be determined!")
        _exit(1)

#end getServer()-------------------------------



"""

 +--------------------------------------------+
 |                                            |
 |  Main Entrypoint                           |
 |                                            |
 +--------------------------------------------+
 
"""



def main():

    # Check if DEBUG mode is set
    setDebug()
    
    # Get python interpreter version
    py3 = getPythonVersion() > 2    
    
    # Display values if in debug mode
    if getDebug():
        
        debugMsg("In debug mode")
        debugMsg("Python version " + str(getPythonVersion()))
        
        if os.environ.get('APIBASE'):
            debugMsg("APIBASE set to '" + os.environ['APIBASE'] + "'")
        if os.environ.get('SERVER'):
            debugMsg("SERVER set to '" + os.environ['SERVER'] + "'")
        if os.environ.get('OWNER'):
            debugMsg("OWNER set to '" + os.environ['OWNER'] + "'")
        if os.environ.get('REPO'):
            debugMsg("REPO set to '" + os.environ['REPO'] + "'")
        if os.environ.get('AUTH'):
            debugMsg("AUTH set to '" + os.environ['AUTH'] + "'")
        if os.environ.get('SCRIPTNAME'):
            debugMsg("SCRIPTNAME set to '" + os.environ['SCRIPTNAME'] + "'")
        if len(sys.argv) > 0:
            debugMsg("Argument list is '" + str(sys.argv) + "'")
        
        print " "
    
    # The first argument should be the name of the method we will use.
    if len(sys.argv) > 0:
        
        if getDebug():
            debugMsg("Calling " + str(sys.argv[1]) + "()")

        # Let's do some work.
        print getScriptName() + ": Fetching..."
        getattr(sys.modules[__name__], str(sys.argv[1]))()
    
    else:
        errMsg("We need the method to run passed in as the first argument.")
        _exit(1)
    

#end main()-------------------------------

def _exit(code):

    """ Performs proper clean up before exiting
    """
    if getDebug():
        debugMsg('Exit code = ' + str(code))
    sys.exit(code)

#end _exit()-------------------------------

if __name__ == "__main__":
    main()