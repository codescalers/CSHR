FROM python:3.8-slim-buster AS poetry
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt

FROM python:3.8-slim-buster
WORKDIR /app
COPY --from=poetry /app/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
