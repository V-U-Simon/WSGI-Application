# 🐍 python image
FROM python:3.11-slim as python-base
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONFAULTHANDLER=1 
ENV PYTHONHASHSEED=random
# 📚 дополнительные библиотеки
RUN apt-get update && apt-get install -y "build-essential"


# 🧰 poetry image
FROM python-base as poetry
ENV POETRY_NO_INTERACTION=1 
ENV POETRY_VERSION=1.3.2
# Установка poetry через pip: /root/.local/bin/poetry
RUN pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false


# packages image
FROM poetry as installed_packages
WORKDIR /opt
COPY poetry.lock pyproject.toml ./
RUN poetry install 


# application image
FROM installed_packages as wsgi_application
WORKDIR /app
COPY . .
EXPOSE 8000

CMD ["gunicorn", "wsgi:application", "-b 0.0.0.0:8000"]
