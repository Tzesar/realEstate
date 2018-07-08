#!/bin/bash

function generic_output_test {
	local status=$1
	if [ $status -ne 0 ]; then
		echo $2
		if [ "$VERBOSE_MODE" = true ]; then
			echo "Check the logfiles for more details [" $LOGFILE "]"
		fi
		exit $status
	fi
}

function python_output_test {
	local status=$?
	generic_output_test $status "Python manage.py error"
}

function git_output_test {
	local status=$?
	generic_output_test $status "Error retrieving data from the repo"
}

echo "Updating project data from repository: "

LOGFILE="deploy.log"
DEBUGLOG=/dev/null
VERBOSE_MODE=false

BRANCH="development"

for arg in "$@"; do
	if [ $arg = "--verbose" ]; then
		VERBOSE_MODE=true
		DEBUGLOG=$LOGFILE
		echo "Verbose mode enabled"
	elif [ $arg = "--prod" ]; then
		BRANCH="master"
	elif [ $arg = "--dev" ]; then
		BRANCH="development"
	fi
done

REPO_URL=$(git remote get-url --all origin)
echo "Retrieving latest changes from repo:" $REPO_URL

git fetch --all >> $DEBUGLOG 2>> $LOGFILE
git_output_test
git checkout "$BRANCH" >> $DEBUGLOG 2>> $LOGFILE
git_output_test
git pull origin "$BRANCH" >> $DEBUGLOG 2>> $LOGFILE
git_output_test

echo "Branch" $BRANCH "updated"

python manage.py migrate >> $DEBUGLOG 2>> $LOGFILE
python_output_test

echo "DB migrated"

python manage.py collectstatic --clear --no-input >> $DEBUGLOG 2>> $LOGFILE
python_output_test

echo "Static files collected"
