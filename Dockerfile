FROM python:2

ENV DEBIAN_FRONTEND=noninteractive \
     CONTAINER_USER=python

RUN apt update && apt remove -yqq python3 --autoremove
RUN apt install -yqq dialog default-mysql-server
RUN sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp
RUN pip install --upgrade pip
RUN mkdir /var/app
WORKDIR /var/app
COPY src/deploy/requirements.txt src/deploy/requirements.txt
RUN pip install MySQL-python
RUN pip install -r src/deploy/requirements.txt
COPY . .
CMD ["./docker-entrypoint.sh"]
