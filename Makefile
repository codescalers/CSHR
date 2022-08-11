
CMD:=poetry run


lint:
	$(CMD) black .
	$(CMD) flake8 .


migrate:
	$(CMD) python3 manage.py migrate