#!/usr/bin/bash

version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
    echo "Python 3 not installed!" 
    exit
fi

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

# cd to project root, where install.sh is located
# (in case the script is called from elsewhere)
cd $SCRIPTPATH

VENV_DIR=${SCRIPTPATH}/venv
if [ -d "$VENV_DIR" ]; then
    echo "venv exists, skipping..."
else 
    echo "venv does not exist, creating..."
    python3 -m venv venv
fi

echo "Sourcing venv..."
source venv/bin/activate

python3 -m pip install -r requirements.txt

if [ ! -f "${SCRIPTPATH}/db.sqlite3" ]; then
    echo "db does not exist, creating..."
    PY_SCRIPT="${SCRIPTPATH}/create_db.py"
    echo $PY_SCRIPT
    python3 $PY_SCRIPT
fi

python3 manage.py migrate
deactivate

exit
