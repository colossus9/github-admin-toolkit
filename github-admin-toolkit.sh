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
#/   -h | --help                                   Display this help message.
#/   -l | --list                                   List available scripts to execute
#/   -p | --proxy <http://proxy.company.com:8080>  Set the web proxy if behind a company firewall (not ready)
#/   -s | --server [github.com|ghe.company.com]    (Required) The GitHub [Enterprise] server to connect
#/   -o | --owner <OWNER>                          The GitHub owner name on the server.
#/   -r | --repo <REPO>                            The GitHub repository name on the server.
#/   -a | --auth <TOKEN>                           Personal Access Token for endpoints that need auth
#    -f | --format [plain|slack|flowdock]          (Optional) Select the output format to use (not ready)
#/   -d | --debug                                  (Optional) If specified, show debug output.
#/   <scriptname>                                  (Required) The name of the script to execute.
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

  header
  . ./utilities/script-list.sh
}

function header
{
  # ------------------------------------------
  # Function to print the header if in debug
  # ------------------------------------------

  if [ -n "$DEBUG" ]; then
    printf "\n"
    printf " ------------------------------------------------------------\n"
    printf "  GitHub Administrator Toolkit\n"
    printf "  $(date)\n"
    printf "  Running $0\n"
    printf "  Args: $ARGS\n"
    printf " ------------------------------------------------------------\n"
    printf "\n"
  fi

}

# Set standard Messages
ERRMSG_NUMOPTS="\nERROR: You must specify options with this script. See the usage message for help.\n"
ERRMSG_UNKOPTS="\nERROR: Unknown option:"

# +---------------------------------------------------------------------------+
# | Get parameters from the command line options.                             |
# +---------------------------------------------------------------------------+

# Reset environment (and set defaults where necessary)
ARGS="$@"
SERVER=
OWNER=
REPO=
LOG="./log/$(basename $0).log"
DEBUG=
LIST=
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
    -p|--proxy)
      export http_proxy="$2"
      export https_proxy="$2"
      shift
      ;;
    -s|--server)
      export SERVER="$2"
      shift
      ;;
    -o|--owner)
      export OWNER="$2"
      shift
      ;;
    -r|--repo)
      export REPO="$2"
      shift
      ;;
    -a|--auth)
      export AUTH="$2"
      shift
      ;;
    -d|--debug)
      export DEBUG=1
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
[[ -n $1 ]] && export SCRIPTNAME="$1"

# Prepare log file (will fix this later)
#mkdir -p $(dirname $LOG)  # Ensure the logging directory exists
#touch $LOG                # Create log file if it doesn't exist
#chmod 777 $LOG            # Make log readable
#exec &> >(tee -a "$LOG")  # Output to stdout and log file

# Check that we have a SERVER to connect to
if [ ! -n "$SERVER" ]; then
  echo -n "Enter the name of the GitHub server (i.e. github.com) and press [ENTER]: "
  read SERVER
  export SERVER=$SERVER
fi

# Check that we have a SCRIPTNAME to work with
if [ ! -n "$SCRIPTNAME" ]; then
  echo -n "Enter the name of the script (i.e. get-collaborators) and press [ENTER]: "
  read SCRIPTNAME
  export SCRIPTNAME=$SCRIPTNAME
fi

# +---------------------------------------------------------------------------+
# | Perform work.                                                             |
# +---------------------------------------------------------------------------+

# Display header
header

# If in debug mode, display values
if [ -n "$DEBUG" ]; then
  printf "\nDisplaying parameter values:\n"
  [ -n "$SERVER" ] && printf "  --> SERVER=$SERVER\n"
  [ -n "$OWNER" ] && printf "  --> OWNER=$OWNER\n"
  [ -n "$REPO" ] && printf "  --> REPO=$REPO\n"
  [ -n "$AUTH" ] && printf "  --> AUTH=$AUTH\n"
  [ -n "$LOG" ] && printf "  --> LOG=$LOG\n"
  [ -n "$SCRIPTNAME" ] && printf "  --> SCRIPTNAME=$SCRIPTNAME\n"
  [ -n "$DEBUG" ] && printf "  --> DEBUG=true\n"
  printf "\n"
fi

# Load the available scripts and perform the work
. ./utilities/script-loader.sh
