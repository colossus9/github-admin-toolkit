#!/usr/bin/env bash
#
# Filename:     api-base.sh
#
# Description:  Build the API base URL depending on whether we are accessing
#               the public github.com or a private GitHub Enterprise server.
#

# Reset environment
APIBASE=
HTTPHEADERS="Accept: application/vnd.github.v3+json"

# Check if we have a valid SERVER parameter
if [ ! -n "$SERVER" ]; then
  echo -n "Enter the name of the GitHub server (i.e. github.com) and press [ENTER]: "
  read SERVER
fi

# Determine if this is for the public github.com
if [ "$SERVER" == "github.com" ]; then
  APIBASE="https://api.github.com"
else
  APIBASE="https://$SERVER/api/v3"
fi

# Check if this is a valid GitHub server
STATUSCODE=0
STATUSCODE=`curl -s -o /dev/null -I -w "%{http_code}" -H "$HTTPHEADERS" $APIBASE/feeds`

if [ "$STATUSCODE" -ne "200" ]; then
  echo "ERROR ($0): The server $SERVER did not return a valid status code. Please check your -s|--server name and try again.";
  exit 1;
else
  echo "INFO ($0): API Base URL '$APIBASE' is valid.";
fi
