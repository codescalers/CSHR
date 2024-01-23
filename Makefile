
CMD:=poetry run
client:=cd client
server:=cd server
terraform:=cd terraform

docker-up:
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up --build -d
docker-down:
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down
install:
	$(server) && pip3 install poetry
	$(server) && poetry install
	$(server) && poetry check
	$(client) && npm i -g pnpm && pnpm i
runserver:
	$(server) && $(CMD) python3 manage.py runserver
runclient:
	$(client) && pnpm i && pnpm dev
test:
	$(CMD) python3 manage.py test
lint:
	$(CMD) black server/  --exclude=__init__.py
	$(CMD) flake8 server/  --exclude=__init__.py
	$(client) && pnpm lint
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
