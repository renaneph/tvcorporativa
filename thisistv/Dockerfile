FROM centos:7

RUN yum -y update && yum -y upgrade 

RUN yum -y install gcc-c++ && yum -y  install python3
RUN yum -y install openssl-devel && yum -y  install wget
RUN yum -y install make && yum -y  install python3-devel
RUN yum -y install mysql-devel && yum -y  install libevent-devel
RUN yum -y install epel-release && yum -y install python3-pip

RUN pip3 install --upgrade pip

WORKDIR /var/www/thisistv
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8000
