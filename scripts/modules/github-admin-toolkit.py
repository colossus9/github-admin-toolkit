#!/usr/bin/env python
#
# Filename:     github-admin-toolkit.py
#
# Description:  Helper module that handles JSON parsing and
#               data processing for the github-admin-toolkit
#

import json
import os
import sys
import urllib2

debug                   = None                                          # Debug mode flag
py3                     = False                                         # Detect python version
acceptHeader            = 'application/vnd.github.v3+json'              # Accept header for HTTP call
acceptHeaderSpiderman   = 'application/vnd.github.spiderman-preview'    # Custom preview header for Traffic endpoint
auth                    = None                                          # If needed, the Authorization token

"""

 +--------------------------------------------+
 |                                            |
 |  GitHub Admin Toolkit                      |
 |                                            |
 +--------------------------------------------+
 
"""

def listUserForks():

    debugMsg('Entered listUserForks()')
    
    # Display the header
    printHeaderMsg('Listing forks for https://' + getServer() + '/' + getOwner() + '/' + getRepo())
    
    # Build and show the output
    getForkInfoForRepo(getRepo())
    
#end listUserForks()()-------------------------------

def getRecentTraffic():

    debugMsg('Entered getRecentTraffic()')

    # Check if the repo was provided
    if os.environ.get('REPO'):
        
        debugMsg('Both OWNER/REPO provided (' + getOwner() + '/' + getRepo() + ')')
        
        # Display the header
        printHeaderMsg('Traffic info for https://' + getServer() + '/' + getOwner() + '/' + getRepo())
        
        # Build and show the output
        getRecentTrafficForRepo(getRepo())
    
    
    else: # Only owner was provided

        debugMsg('Only OWNER provided (' + getOwner() + ')')

        # Get data with the provided owner first
        headers = {'Accept':acceptHeader}
        scheme, code, response = getHTTPResponse(headers, '/orgs/' + getOwner() + '/repos')
        
        # Display the header
        print 'Traffic info for https://' + getServer() + '/' + getOwner()
        
        # Keep track of overall org-level contributions
        dictOrgSummary = {"Referrers":{"Count":0,"Uniques":0},"Paths":{"Count":0,"Uniques":0},"Views":{"Count":0,"Uniques":0},"Clones":{"Count":0,"Uniques":0}}
        
        # Build and display the output, iterate over repos
        full_name = None
        repo = None
        for repos in response:
            for key, value in repos.items():
                if key == 'name':
                    repo = str(value)
                if key == 'full_name':
                    full_name = str(value)
            # Get traffic for this repo
            debugMsg('Getting traffic for ' + full_name)
            print ' '
            printHeaderMsg(full_name)
            dictReferrers, dictPaths, dictViews, dictClones = getRecentTrafficForRepo(repo)
            
            # Add repo results to summary
            for title, dict in dictOrgSummary.items():
                for key, value in dict.items():
                    if title == 'Referrers':
                        dictOrgSummary[title][key] += dictReferrers[key]
                    if title == 'Paths':
                        dictOrgSummary[title][key] += int(dictPaths[key])
                    if title == 'Views':
                        dictOrgSummary[title][key] += int(dictViews[key])
                    if title == 'Clones':
                        dictOrgSummary[title][key] += int(dictClones[key])
        
        # Finally, display summary
        print ' '
        printHeaderMsg(' ** Summary for ' + scheme + '://' + getServer() + '/' + getOwner() + ' ** ')
        
        for title,dict in dictOrgSummary.items():
            print title + ':'
            for key,value in dict.items():
                print '  ' + key + ' ' + str(dict[key])

#end getRecentTraffic()-------------------------------

def getLatestRelease():

    print 'getLatestRelease() Not Yet Implemented. See https://github.com/colossus9/github-admin-toolkit/issues/4'

#end getLatestRelease()-------------------------------

def getContributors():

    debugMsg('Entered getContributors()')

    # Check if the repo was provided
    if os.environ.get('REPO'):

        debugMsg('Both OWNER/REPO provided (' + getOwner() + '/' + getRepo() + ')')
        headers = {'Accept':acceptHeader}
        scheme, code, response = getHTTPResponse(headers, '/repos/' + getOwner() + '/' + getRepo() + '/contributors')

        # Parse data
        debugMsg('Parsing Response Body')

        # Display the header
        printHeaderMsg('Contributors for ' + scheme + '://' + getServer() + '/' + getOwner() + '/' + getRepo())

        # Build the output
        login = None
        contributions = None
        for user in response:
            for key, value in user.items():
                if key == 'login':
                    login = str(value)
                if key == 'contributions':
                    contributions = str(value)
            print str(login + ' (' + scheme + '://' + getServer() + '/' + login + ')' + ' ' + contributions)

    
    else: # Only owner was provided

        debugMsg('Only OWNER provided (' + getOwner() + ')')

        # Get data with the provided owner first
        headers = {'Accept':acceptHeader}
        scheme, code, response = getHTTPResponse(headers, '/orgs/' + getOwner() + '/repos')

        # Parse data
        debugMsg('Parsing Response Body')

        # Print overall header, and then drill down
        print 'Contributors for ' + scheme + '://' + getServer() + '/' + getOwner()

        # Keep track of overall org-level contributions
        dictContributors = {}

        # Build and display the output, iterate over repos
        full_name = None
        for repo in response:
            for key, value in repo.items():
                if key == 'full_name':
                    full_name = str(value)
                    break
            print ' '
            printHeaderMsg(full_name)

            # Get collaborators for this repo
            debugMsg('Getting collaborators for ' + full_name)
            headers = {'Accept':acceptHeader}
            scheme, code, response = getHTTPResponse(headers, '/repos/' + full_name + '/contributors')

            # Parse data
            debugMsg('Parsing Response Body')

            # Build and display the repo output
            login = None
            contributions = None
            for user in response:
                for key, value in user.items():
                    if key == 'login':
                        login = str(value)
                    if key == 'contributions':
                        contributions = str(value)

                # Add to dictionary for summary and print current repo
                if login in dictContributors:
                    dictContributors[login] += int(contributions)
                else:
                    dictContributors[login] = int(contributions)
                print str(login + ' (' + scheme + '://' + getServer() + '/' + login + ')' + ' ' + contributions)

        # Finally, display summary
        print ' '
        printHeaderMsg(' ** Summary for ' + scheme + '://' + getServer() + '/' + getOwner() + ' ** ')

        for key, value in dictContributors.items():
            print str(key + ' (' + scheme + '://' + getServer() + '/' + key + ') ' + str(value))

#end getContributors()-------------------------------



"""

 +--------------------------------------------+
 |                                            |
 |  Helper methods                            |
 |                                            |
 +--------------------------------------------+
 
"""

def getHTTPResponse(headers, path):
    
    debugMsg('Entered getHTTPResponse()')
    
    global auth
    
    # Load appropriate HTTP libs
    try:
        from urllib.request import Request, urlopen, HTTPError, URLError     # Python 3
        from urllib.parse import urlparse, urlsplit
    except:
        from urllib2 import Request, urlopen, HTTPError, URLError            # Python 2
        from urlparse import urlparse, urlsplit
    
    # Build the request object
    scheme = None
    request = None
    url = getAPIBase() + path
    scheme = urlsplit(url).scheme
    request = Request(url)
    
    # Debug msgs
    debugMsg('url = ' + str(url))    
    debugMsg('scheme = ' + str(scheme))
    
    # Set needed header(s)
    for key, value in headers.items():
        request.add_header(key, value)
    
    # Get the response
    try:
        debugMsg('Header items are ' + str(request.header_items()))
        response = urlopen(request)
    except HTTPError as e:
        
        # If HTTP 401 or 403, get auth token and try again
        if str(e.code) == '401' or str(e.code) == '403':
            if 'Authorization' in headers:  # We already tried auth and it didn't work.
                errMsg('HTTP Status Code ' + str(e.code) + '. The Auth token provided was not accepted. Try again using the [-d|--debug] option to check the token. You may also need to be an admin on the repo.')
                debugMsg('Tried auth token: ' + str(headers['Authorization']))
                _exit(1)
                
            else: # We haven't tried auth yet, so let's add it and send the request again
                setAuth()
                headers['Authorization'] = getAuth()
                scheme, code, body = getHTTPResponse(headers, path)
                return scheme, code, body
        
        # If HTTP 404, then not found, check inputs or private repo
        elif str(e.code) == '404':            
            if 'Authorization' in headers:  # We already tried auth and it didn't work.
                errMsg('HTTP Status Code ' + str(e.code) + '. The endpoint was not found. Try again using the [-d|--debug] option to check the token. You may also need to be an admin on the repo.')
                debugMsg('Tried auth token: ' + str(headers['Authorization']))
                _exit(1)
                
            else: # We haven't tried auth yet, so let's add it and send the request again
                setAuth()
                headers['Authorization'] = getAuth()
                scheme, code, body = getHTTPResponse(headers, path)
                return scheme, code, body
        
        # if HTTP 415, then wrong Accept header provided
        elif str(e.code) == '415':
            errMsg('HTTP Status Code ' + str(e.code) + '. The Accept header provided (' + str(headers['Accept']) + ') may be incorrect.')
        
        # Display generic message
        else:
            errMsg('HTTP Status Code ' + str(e.code) + '. Please check your inputs and try again.')
            _exit(1)
            
    except URLError as e:
        errMsg('URLError Exception. Please check the connection string and the network and try again.')
        _exit(1)
    else:
        # Return status and JSON response
        body = json.load(response)
        debugMsg('code=' + str(response.code) + '; body=' + str(body))
        return scheme, response.code, body

#end getHTTPResponse()-------------------------------

def getForkInfoForRepo(repo):
    
    debugMsg('Entered getForkInfoForRepo()')
    
    global acceptHeader
    
    # +----------------------------+
    # | Get Fork Info              |
    # +----------------------------+
    headers = {'Accept' : acceptHeader}
    scheme, code, response = getHTTPResponse(headers, '/repos/' + getOwner() + '/' + repo + '/forks')
    
    # Build the output
    full_name = None
    html_url = None
    for forks in response:
        for key, value in forks.items():
            if key == 'full_name':
                full_name = str(value)
            if key == 'html_url':
                html_url = str(value)
        print str(full_name + ' (' + html_url + ')')
    
#end getForkInfoForRepo()-------------------------------

def getRecentTrafficForRepo(repo):
    
    debugMsg('Entered getRecentTrafficForRepo()')
    
    global acceptHeader
    
    # Let's keep track of the summary
    dictReferrers = {}
    dictPaths = {}
    dictViews = {}
    dictClones = {}
    
    # +----------------------------+
    # | List referrers             |
    # +----------------------------+
    headers = {'Accept' : acceptHeader, 'Authorization' : getAuth()}
    scheme, code, response = getHTTPResponse(headers, '/repos/' + getOwner() + '/' + repo + '/traffic/popular/referrers')

    # Build the output
    print 'Referrers:'
    referrer = None
    count = 0
    uniques = 0
    for referrers in response:
        for key, value in referrers.items():
            if key == 'referrer':
                referrer = str(value)
            if key == 'count':
                count = int(value)
            if key == 'uniques':
                uniques = int(value)
        print str('  ' + referrer + ' (Count ' + str(count) + ', Uniques ' + str(uniques) + ')')
    dictReferrers = {'Count':count,'Uniques':uniques}

    # +----------------------------+
    # | List paths                 |
    # +----------------------------+
    headers = {'Accept' : acceptHeader, 'Authorization' : getAuth()}
    scheme, code, response = getHTTPResponse(headers, '/repos/' + getOwner() + '/' + repo + '/traffic/popular/paths')
    
    # Build the output
    print 'Paths:'
    path = None
    count = 0
    uniques = 0
    for paths in response:
        for key, value in paths.items():
            if key == 'path':
                path = str(value)
            if key == 'count':
                count = int(value)
            if key == 'uniques':
                uniques = int(value)
        print str('  ' + path + ' (Count ' + str(count) + ', Uniques ' + str(uniques) + ')')
    dictPaths = {'Count':count,'Uniques':uniques}

    # +----------------------------+
    # | List views                 |
    # +----------------------------+
    headers = {'Accept' : acceptHeader, 'Authorization' : getAuth()}
    scheme, code, response = getHTTPResponse(headers, '/repos/' + getOwner() + '/' + repo + '/traffic/views')
    
    # Build the output
    print 'Views:'
    count = 0
    uniques = 0
    for key, value in response.items():
        if key == 'count':
            count = int(value)
        if key == 'uniques':
            uniques = int(value)
    print str('  (Count ' + str(count) + ', Uniques ' + str(uniques) + ')')
    dictViews = {'Count':count,'Uniques':uniques}
    
    # +----------------------------+
    # | List clones                 |
    # +----------------------------+
    headers = {'Accept' : acceptHeader, 'Authorization' : getAuth()}
    scheme, code, response = getHTTPResponse(headers, '/repos/' + getOwner() + '/' + repo + '/traffic/clones')
    
    # Build the output
    print 'Clones:'
    count = 0
    uniques = 0
    for key, value in response.items():
        if key == 'count':
            count = int(value)
        if key == 'uniques':
            uniques = int(value)
    print str('  (Count ' + str(count) + ', Uniques ' + str(uniques) + ')')
    dictClones = {'Count':count,'Uniques':uniques}
    
    # Return the summary to the caller
    debugMsg('getRecentTrafficForRepo() return values: Refferers=('+str(dictReferrers)+'); Paths=('+str(dictPaths)+'); Views=('+str(dictViews)+'); Clones=('+str(dictClones))
    return dictReferrers, dictPaths, dictViews, dictClones

#end getRecentTrafficForRepo()-------------------------------

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
    
    return 'token ' + auth

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

def printHeaderMsg(msg):

    print msg
    if py3:
        print('-' * len(msg))
    else:
        print '-' * len(msg)

#end printHeaderMsg()-------------------------------


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
