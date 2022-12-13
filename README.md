# This is a CRM project mainly for the HR department to manage the employees

## To run the project

create .env file and define the environment variables [DJANGO_SECRET_KEY , DJANGO_DEBUG] in it. You can generate yours by using the command in ./config/.env.template

- locally

```sh
cd <repo name>
redis-server --port <port>
poetry install
./manage.py runserver 8000
```
