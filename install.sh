#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

apt-get install python3-tk
mv blanche.py /usr/local/bin/blanche
