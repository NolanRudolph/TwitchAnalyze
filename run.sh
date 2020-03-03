#!/bin/bash

# Check user parameters
if [ "$#" -ne 1 ]; then
	echo "Usage: $ bash run.sh <channel>"
	echo "Ex   : $ bash run.sh trainwreckstv"
	exit 1
fi

CHANNEL=$1

if [ -z $(which python3) ]
then
	apt install -y python3
fi

python3 analyze.py $CHANNEL &

tail -f chat.log;
