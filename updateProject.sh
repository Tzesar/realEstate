#!/bin/bash

echo "Updating project data from repository: "

LOGFILE="deploy.log"
DEBUGLOG=/dev/null

if [ "$1" = "--verbose" ]; then
	DEBUGLOG=$LOGFILE
	echo "Verbose mode enabled"
fi

echo "Retrieving latest changes from repo:" $(git remote get-url --all origin)
git fetch --all >> $DEBUGLOG 2>> $LOGFILE
git checkout master >> $DEBUGLOG 2>> $LOGFILE
git pull origin master >> $DEBUGLOG 2>> $LOGFILE

python manage.py migrate >> $DEBUGLOG 2>> $LOGFILE
python manage.py collectstatic --clear --no-input >> $DEBUGLOG 2>> $LOGFILE
