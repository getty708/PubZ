# PubZ - Publication Zoo
Publication management system for your lab.


## Full Document
[Document](https://getty708.github.io/PubZ/)


## Description
See [Offical Documnet](https://getty708.github.io/PubZ/)

## Requirements
+ Main Host Server
  + docker
  + docker-compose
  



## Instlation
### Step.1 Build Docker Containers
Move to the directory which `docker-compose.yml` exists and issue these commands
```
# Create containers with docker-compose
docker-compose build
# Start containers
docker-compose up 
```
Then, you get 3 containers `db, phpmyadmin, django, (storage)` and each containers are connected each others.


### Step.2 Start Django App
For starting djangp App., you need to initalize database (this system use `mysql`). Issue these commands,

```
# Enter into the django container
docker-compose exec django bash
# Move to the directory (root of the app)
cd app
# Migrate database
python manage.py migrate
# Create Super User
python manage.py createsuperuser
# Migrate Bibtex models
python manage.py makemigrations core
python manage.py migrate
```

For development, use `Username=root, email={any}, pw=password (pwBman88)`

After these commands, please restart all the conatiners.



djangoのコマンドを実行したい場合は以下のコマンドでコンテナの中に入るか、
```
$ docker-compose exec web bash
```
以下のコマンドで直接コマンドを実行することができる.
```
$ docker-compose exec web python3 manage.py migrate
```



### Step.3 Check website
With this setup, we launched 4 containers. You can access to 3 of them with your browser.

| App        | URL              |
|------------|------------------|
| Django     | `localhost:7000` |
| phpmyadmin | `localhost:7070` |
| docs       | `localhost:7777` |


## Usage
[Document](#)を参照.


## Licence
[MIT License](./LICENSE)

