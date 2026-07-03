#!/bin/bash
cd /home/Agustin/Escritorio/Triage/triage_digital
export FORCE_OFFLINE=1
python3 manage.py runserver 0.0.0.0:8000
