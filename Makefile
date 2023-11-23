
CMD:=poetry run
client:=cd client
terraform:=cd terraform

docker-up:
	docker-compose up --build -d
install:
	pip3 install poetry
	poetry install
	poetry check
	cd client && yarn && cd ..
runserver:
	$(CMD) python3 manage.py runserver
runclient:
	$(client) && yarn && yarn run dev
test:
	$(CMD) python3 manage.py test
lint:
	$(CMD) black server/  --exclude=__init__.py
	$(CMD) flake8 server/  --exclude=__init__.py
	$(client) && yarn lint
migrate:
	$(CMD) python3 manage.py makemigrations
	$(CMD) python3 manage.py migrate
user:
	$(CMD) python3 manage.py createsuperuser
data:
	$(CMD) python3 manage.py create locations users
deploy:
	$(terraform) && terraform init && terraform apply -auto-approve
destroy:
	$(terraform) && terraform destroy -auto-approve