# BMAN - Bibtex Management System
Bibtex mangament system which has rich automation functions.


## Full Document
[Document]()


## Description
See [Offical Documnet](#)

## Requirements
+ Main Host Server
  + docker
  + docker-compose
  



## Instlation
### Step.1 Build Docker Containers
Move to the directory which `docker-compose.yml` exists adn issue these command
```
# Create containers with dokcer-compose
docker-compose build
# Start comtainers
docker-compose up 
```
Then, you get 3 containers `db, phpmyadmin, django, (strage)` and each containers are connected each others.


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
python manage.py makemigrateions core
python manage.py migrate
```

For development, use `Username=root, email={any}, pw=password (pwBman88)`

After these command, please restart all the conatiners.



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
Copyright (c) 2018 Yoshimura Naoya, Kato Shinya, Higashide Daiki, Hanxin Wang, Bunki Cao
[MIT License](./LICENSE)

