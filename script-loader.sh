#!/usr/bin/env bash
#
# Filename:     script-loader.sh
#
# Description:  This script will detect runnable scripts in the
#               `./scripts` for consumption by the toolkit. It
#               is called by `github-admin-toolkit.sh` and will
#               list available scripts and their purposes.
#

# Set parameters
SCRIPTDIR="./scripts/"  # Location to search for eligible scripts

# Get the list of eligible scripts to execute with github-admin-toolkit:
for script in `ls -1 $SCRIPTDIR`; do
  echo "$script: `grep '^GITHUB_ADMIN_DESC' <"$SCRIPTDIR\$script"`";
done
