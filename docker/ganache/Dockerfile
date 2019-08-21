FROM node:10.15.3-jessie
LABEL MAINTAINER="Manuel Fernandez manuel.fernandez@balboadevelopers.com"
RUN mkdir /code/

ADD ./solidity /code
RUN npm install -g concurrently
RUN npm install -g ganache-cli
RUN npm install -g truffle

WORKDIR /code/
