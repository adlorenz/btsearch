FROM python:2.7

ENV DEBIAN_FRONTEND=noninteractive \
     CONTAINER_USER=python

RUN apt-get update && apt-get install -yqq default-libmysqlclient-dev
RUN sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp
RUN mkdir /var/app
WORKDIR /var/app
COPY src/deploy/requirements.txt src/deploy/requirements.txt
RUN pip install -r src/deploy/requirements.txt
COPY . .
CMD ["python", "src/manage,py", "runserver", "0.0.0.0:8000"]
