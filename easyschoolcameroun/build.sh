#!/usr/bin/env bash
# Script de construction utilisé par Render.
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
# Base de démonstration (ne fait rien si les variables DEMO_* ne sont pas définies)
python manage.py init_demo || true
