#!/usr/bin/env bash
set -e

python manage.py syncdb
python manage.py migrate
python manage.py "$@"
