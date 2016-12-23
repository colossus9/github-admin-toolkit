#!/usr/bin/env bash
#
# Filename:     script-loader.sh
#
# Description:  This script will detect runnable scripts in the
#               `./scripts/` directory for consumption by the toolkit.
#               If a valid <scriptname> is provided, this utility will
#               execute it and provide the output.
#

# Set parameters
SCRIPTDIR="./scripts/"                 # Location to search for eligible scripts
ENABLED_FILTER="GITHUB_ADMIN_ENABLED=1"  # What to look for when loading scripts
AVAIL_SCRIPTS="./avail-scripts.txt"    # Placeholder to build available scripts table
ISAVAIL=0

# Get the list of eligible scripts to execute with github-admin-toolkit:
rm -rf $AVAIL_SCRIPTS  # Clear the table
for script in `ls -1 $SCRIPTDIR`; do
  if [ "`grep '^GITHUB_ADMIN_ENABLED' <"$SCRIPTDIR\$script"`" == "$ENABLED_FILTER" ]; then
    if [ "$SCRIPTNAME" == "$script" ]; then # The script was found
      ISAVAIL=1;
      break;
    fi;
  fi;
done

# Inform user if none were available
if [ "$ISAVAIL" -ne "1" ]; then
  printf "ERROR: The script '$SCRIPTNAME' is not available. Please try again later.\n\n";
  exit 1;
else
  . ./scripts/$SCRIPTNAME;   # Execute the script if it was found
fi
