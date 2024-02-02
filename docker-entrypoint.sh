#!/bin/sh
set -eu

until mysql -h "${MYSQL_HOST}" -u ${MYSQL_USER} -p ${MYSQL_PASSWORD} ${MYSQL_DATABASE} -e 'select 1'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

python src/manage.py syncdb --noinput
python src/manage.py migrate --noinput
python src/manage.py runserver 0.0.0.0:8000
