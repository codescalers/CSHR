
CMD:=poetry run

install:
	poetry install
	poetry check


run:
	$(CMD) python3 manage.py runserver

test:
	$(CMD) python3 manage.py test

lint:
	$(CMD) flake8 .  --exclude=__init__.py


migrate:
	$(CMD) python3 manage.py makemigrations
	$(CMD) python3 manage.py migrate
