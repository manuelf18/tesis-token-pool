FROM python:3.6.3-stretch
LABEL MAINTAINER="Balboa developers development group"
ENV PYTHONUNBUFFERED 1

RUN apt-get install curl && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash && \
    apt-get install -y nodejs && \ 
    npm install -g truffle
RUN mkdir /code
WORKDIR /code
ADD ./src/requirements/base.txt /code/base.txt
ADD ./src/requirements/development.txt /code/requirements.txt
RUN pip3 install -r requirements.txt
ADD ./src/ /code/
ADD ./utils/ /code/utils/