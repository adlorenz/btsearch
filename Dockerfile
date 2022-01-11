FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive \
     CONTAINER_USER=python

RUN apt-get update && apt-get install -yqq python2-minimal wget python2-dev libmysqlclient-dev mariadb-client gcc
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2.7 get-pip.py
RUN wget https://raw.githubusercontent.com/paulfitz/mysql-connector-c/master/include/my_config.h -O /usr/include/mysql/my_config.h
RUN sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp
RUN pip install --upgrade pip
RUN mkdir /var/app
WORKDIR /var/app
COPY src/deploy/requirements.txt src/deploy/requirements.txt
RUN pip install ConfigParser MySQL-python virtualenv
RUN pip install -r src/deploy/requirements.txt
COPY . .
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
