#!/usr/bin/env bash
#
# Filename:     github-admin-toolkit.sh
#
# Description:  The purpose of this script is to consume admin tools
#               that gather data using the GitHub API. The intent is
#               to take a minimalist approach and keep the code
#               version controlled in GitHub.
#/
#/ -------------------------------------------------------------------
#/ Usage: github-admin-toolkit.sh [options] <scriptname>
#/
#/ Run the specified <scriptname> against a GitHub API server. If authentication
#/ is required, you will be prompted to enter your credentials.
#/
#/ OPTIONS:
#/   -h | --help    Display this help message.
#/   -l | --list    List available scripts to execute
#/   -s | --server  The GitHub [Enterprise] server to connect to (Ex: github.com)
#/   -o | --owner   The GitHub owner name on the server.
#/   -r | --repo    The GitHub repository name on the server.
#/   -d | --debug   (Optional) If specified, show debug output.
#/   <scriptname>   The name of the script to execute.
#/ -------------------------------------------------------------------
#/

set -e

function usage
{
  # ------------------------------------------
  # Function to print error message to console
  # ------------------------------------------

  grep '^#/' <"$0" | cut -c 4-
}

function list
{
  # ------------------------------------------
  # Function to list available toolkit scripts
  # ------------------------------------------

  . ./utilities/script-list.sh
}

# Set standard Messages
ERRMSG_NUMOPTS="\nERROR: You must specify options with this script. See the usage message for help.\n"
ERRMSG_UNKOPTS="\nERROR: Unknown option:"
ERRMSG_SERVER="\nERROR: You must specify a server to connect to with the -s|--server option.\n"
ERRMSG_SCRIPTNAME="\nERROR: You must specify a script to run with the <scriptname> parameter.\n"

# +---------------------------------------------------------------------------+
# | Get parameters from the command line options.                             |
# +---------------------------------------------------------------------------+

# Reset environment (and set defaults where necessary)
ARGS="$@"
RC=0  # Return code
SERVER=
OWNER=
REPO=
LOG="./log/$(basename $0).log"
DEBUG=
SCRIPTNAME=

# Check if any arguments were passed
if [[ $# -eq 0 ]] ; then
  printf "$ERRMSG_NUMOPTS"
  usage
  exit 2
fi

# If single option requested, perform display
[ $# -eq 1 ] &&
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -l|--list)
     list
      exit 0
      ;;
    *)
      printf "$ERRMSG_NUMOPTS"
      usage
      exit 2
      ;;
  esac

# Parse the options
while [ $# -gt 1 ]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -l|--list)
      list
      exit 0
      ;;
    -s|--server)
      SERVER="$2"
      shift
      ;;
    -o|--owner)
      OWNER="$2"
      shift
      ;;
    -r|--repo)
      REPO="$2"
      shift
      ;;
    -d|--debug)
      DEBUG=1
      ;;
    --)
      shift
      break
      ;;
    *)
      printf "$ERRMSG_UNKOPTS $1\n"
      usage
      exit 2
      ;;
  esac
  shift
done

# Get the non-optional/last argument for the SCRIPTNAME
[[ -n $1 ]] && SCRIPTNAME="$1"

# Prepare log file (will fix this later)
#mkdir -p $(dirname $LOG)  # Ensure the logging directory exists
#touch $LOG                # Create log file if it doesn't exist
#chmod 777 $LOG            # Make log readable
#exec &> >(tee -a "$LOG")  # Output to stdout and log file

# Check that we have a SERVER to connect to
if [ ! -n "$SERVER" ]; then
  printf "$ERRMSG_SERVER"
  RC=2  # Return code
fi

# Check that we have a SCRIPTNAME to work with
if [ ! -n "$SCRIPTNAME" ]; then
  printf "$ERRMSG_SCRIPTNAME"
  RC=2  # Return code
fi

# Exit with error if something isn't right. Proceed if we are good
[ "$RC" -ne 0 ] && usage && exit $RC

# +---------------------------------------------------------------------------+
# | Perform work.                                                             |
# +---------------------------------------------------------------------------+
printf "\n"
printf " -----------------------------\n"
printf " $(date)\n"
printf " Running $0\n"
[ -n "$DEBUG" ] && printf " (debug) Args: $ARGS\n"
printf " -----------------------------\n"
printf "\n"

# If in debug mode, display values
if [ -n "$DEBUG" ]; then
  printf "\n(debug) Displaying parameter values:\n"
  [ -n "$SERVER" ] && printf "  --> SERVER=$SERVER\n"
  [ -n "$OWNER" ] && printf "  --> OWNER=$OWNER\n"
  [ -n "$REPO" ] && printf "  --> REPO=$REPO\n"
  [ -n "$LOG" ] && printf "  --> LOG=$LOG\n"
  [ -n "$SCRIPTNAME" ] && printf "  --> SCRIPTNAME=$SCRIPTNAME\n"
  [ -n "$DEBUG" ] && printf "  --> DEBUG=true\n"
  printf "\n"
fi

# Load the available scripts
. ./utilities/script-loader.sh
