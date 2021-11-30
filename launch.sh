#!/usr/bin/bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

VENV_DIR=${SCRIPTPATH}/venv
if [ ! -d "$VENV_DIR" ]; then
    echo "venv does not exist, exiting..."
    exit
fi

source $SCRIPTPATH/venv/bin/activate

if [ ! -f "${SCRIPTPATH}/db.sqlite3" ]; then
    echo "db does not exist, creating..."
    PY_SCRIPT="${SCRIPTPATH}/create_db.py"
    echo $PY_SCRIPT
    python3 $PY_SCRIPT
fi

python3 $SCRIPTPATH/manage.py runserver
