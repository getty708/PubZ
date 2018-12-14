# Dyployment to Kubernetes

## Before Starting
Docker images (pubz, mysql) should be loaded in the worker nodes. You can export and load images with following commands.

In the local PC,

```
# MySQL
cd mysql
docker build -t pubz/mysql:5.7
docker save pubz/mysql:5.7 > pubz.mysql.v5.7.tar 

# Django
cd django
docker build -t pubz/django:v0.2.0 -f Dockerfile-k8s .
docker save pubz/django:v0.2.0  > pubz.django.v0.2.0.tar

```


## Deployment
## MySQL

```
kubectl apply -f mysql/
```

## Django

```
kubectl apply -f django/
```



After making container, connect to bash and run these command to migrate db.

```
cd app
python manage.py makemigrations core users
python manage.py migrate
python manage.py createsuperuser
```
