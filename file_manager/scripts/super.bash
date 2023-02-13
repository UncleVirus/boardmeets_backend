#!/bin/bash

NAME="E-board-daphne"  # Name of the application
DJANGODIR=/home/sudocrack/Desktop/E-board  # Django project directory
DJANGOENVDIR=/home/sudocrack/Desktop/E-board/venv  # Django project env

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/sudocrack/Desktop/E-board/venv/bin/activate
source /home/sudocrack/Desktop/E-board/venv/.env
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start daphne
exec ${DJANGOENVDIR}/bin/daphne eboard_system.asgi:application --port 8000 --bind 0.0.0.0 -v2