# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# == Stage.1: Make requirements.txt by poetry ==
FROM python:3.9-slim as builder
WORKDIR /root/src/
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt


# == Stage.3: Build Minimum Images ==
FROM ubuntu:18.04

# timezone setting
RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata
# timezone setting
ENV TZ=Asia/Tokyo 

# Install required packages and remove the apt packages cache when done.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
		default-libmysqlclient-dev \
		emacs \
		git \
		mysql-client \
		nginx \
		supervisor \
	&& rm -rf /var/lib/apt/lists/*
# Install Python3.8
RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.8-venv \
		libpython3.8-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :
RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH
RUN apt-get update \
	&& apt-get install -y \
		python-pip \
		python3-pip \
	&& pip install --upgrade pip \
	&& pip3 install -U pip setuptools

# encode setting
# set the locale
RUN apt-get clean \
	&& apt-get update \
	&& apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

#don't show error message
ENV DEBCONF_NOWARNINGS yes

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf


COPY ./nginx-app.conf /etc/nginx/sites-available/default
COPY ./supervisor-app.conf /etc/supervisor/conf.d/
COPY ./uwsgi.ini /code/
COPY ./uwsgi_params /code/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY --from=builder /root/src/requirements.txt .
RUN pip3 install -r requirements.txt --no-deps

# add (the rest of) our code
COPY ./src /code/app/

# ENV PYTHONPATH /usr/bin/python3


# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
#RUN django-admin.py startproject website /code/app/

# this line do collectstatic and migrate
# RUN cd /code/app && /usr/bin/python3 manage.py collectstatic --no-input;/usr/bin/python3 manage.py migrate;

EXPOSE 8080
CMD ["supervisord", "-n"]
