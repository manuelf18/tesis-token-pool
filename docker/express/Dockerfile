FROM node:12.7-stretch
LABEL MAINTAINER="Manuel Fernández manuel.fernandez4@utp.ac.pa"
RUN mkdir /code/

ADD ./src/api /code/
RUN npm install -g nodemon
RUN npm install --verbose

WORKDIR /code/