
CMD:=poetry run
client:=cd client
server:=cd server
terraform:=cd terraform

docker-up:
ifeq ($(service), frontend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up frontend --build -d
else ifeq ($(service), backend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up backend --build -d
else ifeq ($(service), postgres)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up postgres --build -d
else
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up --build -d
endif

docker-down:
ifeq ($(service), frontend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down -d frontend
else ifeq ($(service), backend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down -d backend
else ifeq ($(service), postgres)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down -d postgres
else
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down -v
endif

docker-logs:
ifeq ($(service), frontend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs frontend
else ifeq ($(service), backend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs backend
else ifeq ($(service), postgres)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs postgres
else
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs
endif

install:
	$(server) && poetry install
	$(server) && poetry check
	$(client) && pnpm i
runserver:
	$(server) && $(CMD) python3 manage.py runserver
runclient:
	$(client) && pnpm i && pnpm dev
test:
	$(server) && $(CMD) python3 manage.py test
lint:
	$(server) && $(CMD) black .  --exclude=__init__.py
	$(server) && $(CMD) flake8 .  --exclude=__init__.py
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
