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
  APIBASE="https://api.github.com";
  printf "Checking GitHub API connectivity...";
else
  APIBASE="https://$SERVER/api/v3";
  printf "Checking connectivity to GitHub Enterprise at '$APIBASE'...";
fi

# Verify the endpoint is available
if curl --fail -s -o "/dev/null" -H "$HTTPHEADERS" $APIBASE; then
  printf "OK\n\n";
else
  printf "\nERROR: The provided endpoint is not valid.\n\n";
  exit 1;
fi
