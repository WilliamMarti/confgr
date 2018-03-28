FROM tiangolo/uwsgi-nginx-flask:flask
MAINTAINER William Marti "william.b.marti@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install sqlite3 libsqlite3-dev -y
COPY ./confgr /confgr
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
WORKDIR /confgr
ENTRYPOINT ["python"]
CMD ["/confgr/confgr.py"]