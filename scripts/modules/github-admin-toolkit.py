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
acceptHeader    = 'application/vnd.github.v3+json'  # Accept header for HTTP call
auth            = None                              # If needed, the Authorization token



"""

 +--------------------------------------------+
 |                                            |
 |  GitHub Admin Toolkit                      |
 |                                            |
 +--------------------------------------------+
 
"""



def getContributors():

    debugMsg('Entered getContributors()')
    
    # Check if the repo was provided
    if os.environ.get('REPO'):
        
        debugMsg('Both OWNER/REPO provided (' + getOwner() + '/' + getRepo() + ')')
        code, response = getHTTPResponse('/repos/' + getOwner() + '/' + getRepo() + '/contributors')
        
        # Parse data
        debugMsg('Parsing Response Body')
        for item in response:
            for key, value in item.items():
                if key == 'login':
                    print value #+ '(' + getGitHubUser(value) + ')'

    else:
        
        debugMsg('Only OWNER provided (' + getOwner() + ')')
        
        # Get data with the provided owner first
        code, response = getHTTPResponse('/orgs/' + getOwner())
    

#end getContributors()-------------------------------



"""

 +--------------------------------------------+
 |                                            |
 |  Helper methods                            |
 |                                            |
 +--------------------------------------------+
 
"""

def getHTTPResponse(path):
    
    debugMsg('Entered getHTTPResponse()')
    
    global auth
    
    # Build the request object
    request = None
    url = getAPIBase() + path
    
    debugMsg('url is ' + str(url))
    
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
        debugMsg('Using Authentication Header')            
        request.add_header('Authorization', getHTTPHeader('Authorization'))
    
    # Get the response
    try:
        debugMsg('Header items are ' + str(request.header_items()))
        response = urlopen(request)
    except HTTPError as e:
        errMsg('HTTP Status Code ' + str(e.code) + '. Please check your inputs and try again.')
        _exit(1)
    except URLError as e:
        errMsg('URLError Exception. Please check the connection string and the network and try again.')
        _exit(1)
    else:
        # Return status and JSON response
        debugMsg('code=' + str(response.code) + '; body=' + str(response)
        return response.code, json.load(response)

#end getHTTPResponse()-------------------------------

def getGitHubUser(username):
    
    debugMsg('Entered getGitHubUser()')
    
    # Define the GitHub User
    gitHubUser = None
    name = None
    email = None
    
    # Use API call to get user data
    code, response = getHTTPResponse('/users/' + username)
    
    # Parse the data
    for item in response:
        for key, value in item.items():
            if key == 'name':
                name = value
            if key == 'email':
                email = value
    
    # Format the name before returning it
    gitHubUser = name + ' <' + email + '>'
    
    return gitHubUser
    
#end getGitHubUser()-------------------------------

def getPythonVersion():
    
    debugMsg('Entered getPythonVersion()')
    
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

    if getDebug():
        print sys.argv[0] + ': ' + msg
    
#end debugMsg()-------------------------------

def errMsg(msg):
    
    debugMsg('Entered errMsg()')
    
    print 'ERROR (' + sys.argv[0] + '): ' + msg
    
#end errMsg()-------------------------------

def getAPIBase():
    
    debugMsg('Entered getAPIBase()')
    
    # Get the value for the APIBASE
    
    if os.environ.get('APIBASE'):
        return str(os.environ['APIBASE'])
    
    else:
        
        userInput = 'Enter the API base url of the GitHub server (i.e. https://api.github.com) and press [ENTER]: '
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getAPIBase()-------------------------------

def getServer():
    
    debugMsg('Entered getServer()')
    
    # Get the value for the SERVER
    
    if os.environ.get('SERVER'):
        return str(os.environ['SERVER'])
    
    else:
        
        userInput = 'Enter the name of the GitHub SERVER and press [ENTER]: '
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getServer()-------------------------------

def getHTTPHeader(header):
    
    debugMsg('Entered getHTTPHeader()')
    
    global httpHeaders
    global acceptHeader
    
    # Set the recommended Accept header
    httpHeaders['Accept'] = acceptHeader
    
    # Check if we are requesting an Authorization header
    if header == 'Authorization':
        httpHeaders[header] = 'token ' + getAuth()
    
    return httpHeaders[header]

#end getHTTPHeader()-------------------------------

def getOwner():
    
    debugMsg('Entered getOwner()')
    
    # Get the value for the OWNER
    
    if os.environ.get('OWNER'):
        return str(os.environ['OWNER'])
    
    else:
        
        userInput = 'Enter the name of the GitHub OWNER and press [ENTER]: '
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getOwner()-------------------------------

def getRepo():
    
    debugMsg('Entered getRepo()')
    
    # Get the value for the REPO
    
    if os.environ.get('REPO'):
        return str(os.environ['REPO'])
    
    else:
        
        userInput = 'Enter the name of the GitHub REPO and press [ENTER]: '
        if py3:
            return str(input(userInput))
        else:
            return str(raw_input(userInput))

#end getRepo()-------------------------------

def getAuth():
    
    debugMsg('Entered getAuth()')
    
    global auth
    
    if auth == None:
        setAuth()
    
    return auth

#end getRepo()-------------------------------

def setAuth():
    
    debugMsg('Entered setAuth()')
    
    global auth
    
    # Get the value for the AUTH token
    
    if os.environ.get('AUTH'):
        auth = str(os.environ['AUTH'])
    
    else:
        
        print 'Enter a GitHub Personal Access Token to authenticate with and press [ENTER]';
        print '(Note: A token for this server can be created at https://' + str(getServer()) + '/settings/tokens)';
        
        userInput = ': '
        token = ''
        
        if py3:
            auth = str(input(userInput))
        else:
            auth = str(raw_input(userInput))

#end setAuth()-------------------------------

def getScriptName():
    
    debugMsg('Entered getScriptName()')
    
    # Get the value for the SCRIPTNAME
    
    if os.environ.get('SCRIPTNAME'):
        return str(os.environ['SCRIPTNAME'])
    
    else:
        errMsg('The SCRIPTNAME could not properly be determined!')
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
    
    debugMsg('Entered main()')

    # Check if DEBUG mode is set
    setDebug()
    
    # Get python interpreter version
    py3 = getPythonVersion() > 2    
    
    # Display values if in debug mode
    debugMsg('In debug mode')
    debugMsg('Python version ' + str(getPythonVersion()))
        
    if os.environ.get('APIBASE'):
        debugMsg('APIBASE set to ' + os.environ['APIBASE'])
    if os.environ.get('SERVER'):
        debugMsg('SERVER set to ' + os.environ['SERVER'])
    if os.environ.get('OWNER'):
        debugMsg('OWNER set to ' + os.environ['OWNER'])
    if os.environ.get('REPO'):
        debugMsg('REPO set to ' + os.environ['REPO'])
    if os.environ.get('AUTH'):
        debugMsg('AUTH set to ' + os.environ['AUTH'])
    if os.environ.get('SCRIPTNAME'):
        debugMsg('SCRIPTNAME set to ' + os.environ['SCRIPTNAME'])
    if len(sys.argv) > 0:
        debugMsg('Argument list is ' + str(sys.argv))
    
    debugMsg(' ')
    
    # The first argument should be the name of the method we will use.
    if len(sys.argv) > 0:
        
        debugMsg('Calling ' + str(sys.argv[1]) + '()')

        # Let's do some work.
        debugMsg(getScriptName() + ': Fetching...')
        
        try:
            getattr(sys.modules[__name__], str(sys.argv[1]))()  # Call the method with the name of the first argument
        except Exception as e:
            errMsg('Problem encountered while running ' + str(sys.argv[1]) + '; ' + str(e))
    
    else:
        errMsg('We need the method to run passed in as the first argument.')
        _exit(1)
    

#end main()-------------------------------

def _exit(code):
    
    debugMsg('Entered _exit(code)')

    """ Performs proper clean up before exiting
    """
    debugMsg('Exit code = ' + str(code))
    sys.exit(code)

#end _exit()-------------------------------

if __name__ == "__main__":
    main()
