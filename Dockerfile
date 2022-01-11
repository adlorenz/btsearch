FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive \
     CONTAINER_USER=python

RUN apt update && apt install -yqq python2-minimal wget
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2.7 get-pip.py
RUN apt install -yqq libmysqlclient-dev
RUN apt install -yqq mysql-server gcc
RUN sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp
RUN pip install --upgrade pip
RUN mkdir /var/app
WORKDIR /var/app
COPY src/deploy/requirements.txt src/deploy/requirements.txt
RUN pip install ConfigParser MySQL-python virtualenv
RUN pip install -r src/deploy/requirements.txt
COPY . .
CMD ["python", "src/manage,py", "runserver", "0.0.0.0:8000"]
