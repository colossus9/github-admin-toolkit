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
export SCRIPTDIR="./scripts/"                 # Location to search for eligible scripts
export ENABLED_FILTER="GITHUB_ADMIN_ENABLED=1"  # What to look for when loading scripts
export AVAIL_SCRIPTS="./avail-scripts.txt"    # Placeholder to build available scripts table
export ISAVAIL=0

# Debug
[ -n "$DEBUG" ] && echo "Running script-loader.sh"

# Get the list of eligible scripts to execute with github-admin-toolkit:
rm -rf $AVAIL_SCRIPTS  # Clear the table
for script in `ls -1 $SCRIPTDIR`; do
  if [ -f "$SCRIPTDIR/$script" ]; then  # Check that the script is a regular file
    if [ "`grep '^GITHUB_ADMIN_ENABLED' < $SCRIPTDIR/$script`" == "$ENABLED_FILTER" ]; then
      if [ "$SCRIPTNAME" == "$script" ]; then # The script was found
        export ISAVAIL=1;
        break;
      fi;
    fi;
  fi;
done

# Inform user if none were available
if [ "$ISAVAIL" -ne "1" ]; then
  printf "\nERROR: The script '$SCRIPTNAME' is not available. List the available scripts with \`./github-admin-toolkit.sh --list\`\n\n";
  exit 1;
else
  . ./utilities/api-base.sh; # Build and check the API Base URL
  . ./scripts/$SCRIPTNAME;   # Execute the script if it was found
fi
