FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update

# Emacsのインストール
RUN apt-get update
RUN apt-get install emacs24-nox -y

# MySQLクライアントとPythonドライバ
RUN apt-get install -y mysql-client
RUN pip3 install -r requirements.txt
RUN pip3 install PyMySQL

ADD . /code/
