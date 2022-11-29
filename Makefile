
CMD:=poetry run
client:=cd client
terraform:=cd terraform

docker-up:
	docker-compose up --build -d
install:
	poetry install
	poetry check
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
terraform-up:
	$(terraform) && terraform init && terraform apply -parallelism=1 -auto-approve
terraform-down:
	$(terraform) && terraform destroy -parallelism=1 -auto-approve