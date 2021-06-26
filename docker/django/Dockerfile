# == Stage.1: Make requirements.txt by poetry ==
FROM python:3.9-slim as builder
WORKDIR /root/src/
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt

# == Stage.3: Build Minimum Images ==
FROM python:3.9
ENV PYTHONUNBUFFERED 1
VOLUME /code/
WORKDIR /code

# == Ubuntu Packages ==
RUN apt-get update \
    && apt-get install -y \
        emacs24-nox \
        mysql-common \
        mariadb-client

# Install Jupyter
RUN echo 'alias python=python3' >> ~/.bashrc
COPY --from=builder /root/src/requirements.txt .
RUN pip install -r /requirements.txt

