
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
	$(client) && npm install && npm run dev
test:
	$(CMD) python3 manage.py test
lint:
	$(CMD) flake8 .  --exclude=__init__.py
migrate:
	$(CMD) python3 manage.py makemigrations
	$(CMD) python3 manage.py migrate
user:
	$(CMD) python3 manage.py createsuperuser
	$(CMD) python3 manage.py runserver
deploy:
	$(terraform) && terraform init && terraform apply -auto-approve
destroy:
	$(terraform) && terraform destroy -auto-approve