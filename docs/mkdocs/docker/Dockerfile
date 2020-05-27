FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /docs
WORKDIR /docs
RUN apt-get update

# MySQLクライアントとPythonドライバ
RUN pip3 install mkdocs
RUN pip3 install mkdocs-material 
RUN pip3 install python-markdown-math
