
CMD:=poetry run
client:=cd client
server:=cd server
terraform:=cd terraform

docker-up:
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up --build -d
docker-down:
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down -v
install:
	curl -sSL https://install.python-poetry.org | python3 -
	$(server) && poetry install
	$(server) && poetry check
	$(client) && npm i -g pnpm && pnpm i
runserver:
	$(server) && $(CMD) python3 manage.py runserver
runclient:
	$(client) && pnpm i && pnpm dev
test:
	$(server) && $(CMD) python3 manage.py test
lint:
	$(server) && $(CMD) black server/  --exclude=__init__.py
	$(server) && $(CMD) flake8 server/  --exclude=__init__.py
	$(client) && pnpm lint
migrate:
	$(server) && $(CMD) python3 manage.py makemigrations
	$(server) && $(CMD) python3 manage.py migrate
user:
	$(server) && $(CMD) python3 manage.py createsuperuser
data:
	$(server) && $(CMD) python3 manage.py create locations users
deploy:
	$(terraform) && terraform init && terraform apply -auto-approve
destroy:
	$(terraform) && terraform destroy -auto-approve
