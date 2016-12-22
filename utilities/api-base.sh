#!/usr/bin/env bash
#
# Filename:     api-base.sh
#
# Description:  Build the API base URL depending on whether we are accessing
#               the public github.com or a private GitHub Enterprise server.
#

# Reset environment
APIBASE=
HTTPHEADERS="Accept: applican/vnd.github.v3+json"

# Check if we have a valid SERVER parameter
if [ ! -n "$SERVER" ]; then
  echo "ERROR ($0): The SERVER parameter is empty.";
  exit 2;
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






echo "INFO ($0): API Base URL is '$APIBASE'";
