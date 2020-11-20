# pull official base image
FROM python:3.8.6-slim-buster

# set working directory
WORKDIR /usr/src/app

# copy requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./.pylintrc /usr/src/app/.pylintrc

# Updates packages and install git(required for coveralls)
RUN apt-get update
RUN apt-get -y install git

# install dependencies
RUN pip install -r requirements.txt

# copy app
COPY . /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID
ENV FIREBASE-CLIENT-CERT-URL=$FIREBASE-CLIENT-CERT-URL
ENV FIREBASE-CLIENT-EMAIL=$FIREBASE-CLIENT-EMAIL
ENV FIREBASE-CLIENT-ID=$FIREBASE-CLIENT-ID
ENV FIREBASE-PRIVATE-KEY=$FIREBASE-PRIVATE-KEY
ENV FIREBASE-PRIVATE-KEY-ID=$FIREBASE-PRIVATE-KEY-ID
ENV FIREBASE-PROJECT-ID=$FIREBASE-PROJECT-ID
ENV FIREBASE-STORAGE-BUCKET=$FIREBASE-STORAGE-BUCKET

# docker entrypoint for heroku
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
