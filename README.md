# PubZ - Publication Zoo
Publication management system for your lab.

## Full Document

[Document](https://getty708.github.io/PubZ/)

## Requirements

- docker
- docker-compose
- (poetry)

## Instlation (Dev Environment)

Here, let's install PubZ app for development environemnt.
For production use, see [./deploy](./deploy).

### Step.Make DB's Configuration File 

Make `PubZ/.env` and `PubZ/deploy/.env`.

Example:

```shell
MYSQL_ROOT_PASSWORD=mJKB26xRuY
MYSQL_DATABASE=docker
MYSQL_USER=docker
MYSQL_PASSWORD=ipTVFzI5Hx
DJANGO_SECRET_KEY="a10^j@6^2q$y*c&ks29$gnb7*3eodvqp!4!$7h31mlsq0ad3+s"
VIRTUAL_HOST="pubz.example.com"
```

**WARNING: Please change secret key by yorself for production mode. To generate own key, check [here](https://qiita.com/frosty/items/bb5bc1553f452e5bb8ff).**


```python
# Generate Secret Key
from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)
print(text)
```

### Step.1 Build Docker Containers

Move to the directory which `docker-compose.yml` exists and issue these commands

```bash
# Create Storage Directory
mkdir -p ./storage/db/data
# Create docker image with make command
cd docker/django
make build
# Start containers
cd ../../
docker-compose up 
```

Then, you get 3 containers `db, phpmyadmin, django, (storage)` and each containers are connected each others.

### Step.2 Initalize Django App

For starting django App, you need to initalize database (this system use `mysql`). Issue these commands,

```bash
# Enter into the django container
docker-compose exec django bash
```

```bash
# == In django container ==
# Migrate database
python manage.py migrate
# Create Super User
python manage.py createsuperuser
# Migrate Bibtex models
python manage.py makemigrations core
python manage.py migrate
# Collect static files (e.g., js, css)
python manage.py collectstatic
```

For development, use `Username=root, email=test@test.com, pw=password (pwBman88)`

After these commands, please restart all the conatiners.

### Step.3 Start Development Servers

Django application:

```bash
# == In django container ==
cd /code
bash run
```

PubZ docs (dev server):

```bash
# == In django container ==
$ cd /root/docs/mkdocs
$ mkdocs serve
```

### Step.4 Check website

With this setup, we launched 3 containers. You can access to 3 of them with your browser.


| App        | URL              |
|------------|------------------|
| Django     | http://localhost:7000 |
| phpmyadmin | http://localhost:7070 |
| docs       | http://localhost:7777 |

---

## Setup Production Server

```bash
# Create Image with make command
cd docker/django-uwsgi-nginx/
make build
# Start containers
cd ../../
docker-compose -f docker-compose-prd.yaml up -d
```

### Container and Ports

| App        | Container Name   | Port (External) |
|------------|------------------|-----------------|
| Django     | pubz-web-prd     | 8000            |
| MarinaDB   | pubz-db-prd      | 3306            |

---
## Licence

[MIT License](./LICENSE)
