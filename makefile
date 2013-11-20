.PHONY: install remove_pyc update_virtualenv remove_db create_db

install: remove_pyc update_virtualenv remove_db create_db load_fixtures

remove_pyc:
	-find . -type f -name "*.pyc" -delete

update_virtualenv:
	pip install -r www/deploy/requirements.txt

remove_db:
	python www/manage.py reset_db --router=default --noinput

create_db:
	python www/manage.py syncdb --noinput
	python www/manage.py migrate

load_fixtures:

test:
	www/runtests.sh

ci: install test
