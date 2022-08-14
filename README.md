This is a CRM project mainly for the HR department to manage the employees.

# To run the project:
create .env file and define the environment variables [DJANGO_SECRET_KEY , DJANGO_DEBUG] in it.
# locally

```
cd <repo name>
./manage.py runserver 8000
```

# via docker
```
cd <repo name>
docker build -t <image name> .
docker run -p <the port you want to run the project on>:8000 <image name>
```