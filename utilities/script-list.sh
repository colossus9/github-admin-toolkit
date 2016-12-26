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
export SCRIPTDIR="./scripts/"                 # Location to search for eligible scripts
export ENABLED_FILTER="GITHUB_ADMIN_ENABLED=1"  # What to look for when loading scripts
export AVAIL_SCRIPTS="./avail-scripts.txt"    # Placeholder to build available scripts table
export ISAVAIL=0

# Debug
[ -n "$DEBUG" ] && echo "Running script-list.sh"

# Get the list of eligible scripts to execute with github-admin-toolkit:
printf "\n  The following is a list of available scripts:\n\n"
rm -rf $AVAIL_SCRIPTS  # Clear the table
echo "SCRIPTNAME:DESCRIPTION" >> $AVAIL_SCRIPTS
echo "----------:-----------" >> $AVAIL_SCRIPTS
for script in `ls -1 $SCRIPTDIR`; do
  if [ -f "$SCRIPTDIR/$script" ]; then  # Check that the script is a regular file first
    if [ "`grep '^GITHUB_ADMIN_ENABLED' < $SCRIPTDIR\$script`" == "$ENABLED_FILTER" ]; then
      export ISAVAIL=1;
      echo "$script:`grep '^GITHUB_ADMIN_DESC' <"$SCRIPTDIR\$script" | cut -d '"' -f2`" >> $AVAIL_SCRIPTS;
    fi;
  fi;
done

# Inform user if none were available
[ "$ISAVAIL" -ne "1" ] && echo "<none>" >> $AVAIL_SCRIPTS;

# Display the table
column -t -s ":" $AVAIL_SCRIPTS
rm -rf $AVAIL_SCRIPTS  # Clear the table
printf "\n"

# Now remind the user how to utilize these scripts
printf "  To execute a script, use \`./github-admin-toolkit.sh --help\` to see a list of available options.\n\n"
