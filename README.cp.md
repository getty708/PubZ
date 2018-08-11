# BibRich
Bibtex mangament system which has rich automation functions.


## Full Document
[Document]()


## Discription
See [Offical Documnet](#)

## Requirement
+ Main Host Server
  + docker
  + docker-compose
  



## Instlation
まず、dockerをインストールする。以下のサイトを参考に
+ docker installation[https://docs.docker.com/engine/installation/]
+ docker-compose installation[https://docs.docker.com/compose/install/]

dockerをインストールしたのち、`docker-comose.yml`があるディレクトリで以下のコマンドを実行する。
```bash
# コンテナの作成
$ docker-compose build 
# コンテナ同士のリンク関係を構築
$ docker-compose up -d
# コンテナの実行
$ docker-compose up
# コンテナの停止
$ docker-compose down
```
この時点ではコンテナが動かない可能性が高いので、以下のコマンドでデータベースの初期化を行う。
```bash
$ docker-compose run web
$ docker-compose exec web python3 manage.py migrate
# 管理者アカウントの追加
$ docker-compose exec web python3 manage.py createsuperuser
```
ex. `user='root', email='cardinal.sysyem@tafdata.com', PW='password1234'`




djangoのコマンドを実行したい場合は以下のコマンドでコンテナの中に入るか、
```
$ docker-compose exec web bash
```
以下のコマンドで直接コマンドを実行することができる.
```
$ docker-compose exec web python3 manage.py migrate
```


## Usage
[Document](#)を参照.


## Licence
Copyright (c) 2018 Yoshimura Naoya, Kato Shinya, Higashide Daiki, Hanxin Wang, Bunki Cao
[MIT License](./LICENSE)

