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
ENV FIREBASE_CLIENT_CERT_URL=$FIREBASE_CLIENT_CERT_URL
ENV FIREBASE_CLIENT_EMAIL=$FIREBASE_CLIENT_EMAIL
ENV FIREBASE_CLIENT_ID=$FIREBASE_CLIENT_ID
ENV FIREBASE_PRIVATE_KEY=$FIREBASE_PRIVATE_KEY
ENV FIREBASE_PRIVATE_KEY_ID=$FIREBASE_PRIVATE_KEY_ID
ENV FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID
ENV FIREBASE_STORAGE_BUCKET=$FIREBASE_STORAGE_BUCKET

# docker entrypoint for heroku
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
