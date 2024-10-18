FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /app

RUN python manage.py collectstatic --noinput

# Указываем, что приложение будет слушать на порту 8000
EXPOSE 8000

# Запускаем сервер Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]