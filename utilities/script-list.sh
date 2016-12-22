#!/usr/bin/env bash
#
# Filename:     script-list.sh
#
# Description:  This script will detect runnable scripts in the
#               `./scripts/` directory for consumption by the toolkit.
#               It is called by `github-admin-toolkit.sh` and will
#               list available scripts and their purposes.
#

# Set parameters
SCRIPTDIR="./scripts/"                 # Location to search for eligible scripts
ENABLED_FILTER="GITHUB_ADMIN_ENABLED=1"  # What to look for when loading scripts

# Get the list of eligible scripts to execute with github-admin-toolkit:
printf "\nAvailable scripts:\n\n  -----------------------------------------"
for script in `ls -1 $SCRIPTDIR`; do
  if [ "`grep '^GITHUB_ADMIN_ENABLED' <"$SCRIPTDIR\$script"`" == "$ENABLED_FILTER" ]; then
    printf "\n  $script: `grep '^GITHUB_ADMIN_DESC' <"$SCRIPTDIR\$script" | cut -d '"' -f2`\n";
  fi
done
printf "  -----------------------------------------\n"
