FROM python:3.8-slim-buster AS build

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -g 1001 appuser \
    && useradd -r -u 1001 -g appuser appuser \
    && mkdir /home/appuser/ \
    && chown -R appuser:appuser /home/appuser/\
    && chown -R appuser:appuser /app

USER appuser:appuser

RUN python3 -m pip install --upgrade pip

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN /home/appuser/.local/bin/poetry export -f requirements.txt -o requirements.txt



FROM python:3.8-slim-buster

WORKDIR /app

RUN groupadd -g 1001 appuser \
    && useradd -r -u 1001 -g appuser appuser \
    && mkdir /home/appuser/ \
    && chown -R appuser:appuser /home/appuser/\
    && chown -R appuser:appuser /app

COPY --from=build /app/requirements.txt .

USER appuser

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
