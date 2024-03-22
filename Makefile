python = venv/bin/python
pip = venv/bin/pip
pytest = venv/bin/pytest

up:
	docker-compose up -d

pull:
	docker-compose pull

down:
	docker-compose down

db-makemigrations:
	$(python) pastebin/manage.py makemigrations

db-migrate:
	$(python) pastebin/manage.py migrate

db-full-migrate:
	$(python) pastebin/manage.py makemigrations
	$(python) pastebin/manage.py migrate




uninstall-unrequired-libraries:
	$(pip) freeze | grep -v -f requirements.txt - | grep -v '^#' | xargs $(pip) uninstall -y || echo "OK, you dont have any unrequired libraries"

install: uninstall-unrequired-libraries
	$(pip) install -r requirements.txt

install-venv:
	python -m virtualenv venv --python python3

update-requirements:
	$(pip) freeze > requirements.txt

test: clean up
	mkdir -p logs
	$(pytest) -vvvv tests

coverage: clean up
	mkdir -p logs
	$(pytest) --cov-config=./pyproject.toml --cov=src tests/ --cov-report term-missing

clean-logs:
	rm -f logs/*.log
	rm -f logs/*.log.jsonl

clean-test-reports:
	mkdir -p test_reports
	rm -f test_reports/*.xml

clean: clean-logs clean-test-reports


run-pgadmin:
	docker rm -f pgadmin
	docker run --name pgadmin --net=host -e "PGADMIN_DEFAULT_EMAIL=admin@admin.com" -e "PGADMIN_DEFAULT_PASSWORD=admin" -d dpage/pgadmin4
