#!/usr/bin/bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

VENV_DIR=${SCRIPTPATH}/venv
if [ ! -d "$VENV_DIR" ]; then
    echo "venv does not exist, exiting..."
    exit
fi

source $SCRIPTPATH/venv/bin/activate

python3 $SCRIPTPATH/manage.py runserver
