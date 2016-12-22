#!/usr/bin/env bash
#
# Filename:     script-loader.sh
#
# Description:  This script will detect runnable scripts in the
#               `./scripts/` directory for consumption by the toolkit.
#               If a valid <scriptname> is provided, this utility will
#               execute it and provide the output.
#

echo "script-loader"

# Set parameters
SCRIPTDIR="./scripts/"                 # Location to search for eligible scripts
ENABLED_FILTER="GITHUB_ADMIN_ENABLED=1"  # What to look for when loading scripts

# Get the list of eligible scripts to execute with github-admin-toolkit:
for script in `ls -1 $SCRIPTDIR`; do
  if [ "`grep '^GITHUB_ADMIN_ENABLED' <"$SCRIPTDIR\$script"`" == "$ENABLED_FILTER" ]; then
    echo "$script: `grep '^GITHUB_ADMIN_DESC' <"$SCRIPTDIR\$script" | cut -d '"' -f2`";
  fi
done
