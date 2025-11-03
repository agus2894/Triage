#!/bin/bash

echo " Optimizando sistema..."

if [ ! -f "manage.py" ]; then
    echo "Ejecutar desde directorio triage_digital/"
    exit 1
fi

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py optimize_db

mkdir -p logs
touch logs/triage.log

echo " Optimización completada"