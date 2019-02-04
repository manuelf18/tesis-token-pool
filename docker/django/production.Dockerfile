FROM python:3.6.3-stretch
LABEL MAINTAINER="Balboa developers development group"
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN mkdir /code
WORKDIR /code
ADD ./src/requirements/base.txt /code/base.txt
ADD ./src/requirements/production.txt /code/requirements.txt
RUN pip install -r requirements.txt
ADD ./src/ /code/
ADD ./utilities/ /code/utilities/
