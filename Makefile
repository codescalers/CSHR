
CMD:=poetry run
up:
	docker-compose up --build -d
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
user:
	$(CMD) python3 manage.py createsuperuser
	$(CMD) python3 manage.py sqlmigrate cshr 0006
	



user:
	$(CMD) python3 manage.py createsuperuser