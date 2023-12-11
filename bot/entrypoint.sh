#!/usr/bin/env bash

# https://github.com/lightningnetwork/lnd/blob/master/docker/lnd/start-lnd.sh#L64

# exit from script if error was raised.
set -e

# error function is used within a bash function in order to send the error
# message directly to the stderr output and exit.
error() {
    echo "$1" > /dev/stderr
    exit 0
}

# setting timezone
echo "export TZ=\"/usr/share/zoneinfo/Europe/Zurich\"" >>  ~/.bashrc 


# run the software
./main.py 
