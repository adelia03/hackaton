FROM matthewfeickert/docker-python3-ubuntu:latest

ENV PYTHONUNBUFFERED True

WORKDIR /

COPY . .

USER root

RUN apt-get update 
RUN apt-get install -y apt-utils

RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install gunicorn
RUN pip install -r req.txt

ENV SECRET_KEY=^x+-*4zg+lix388k=rmtzqf6
ENV DB_USER=postgres
ENV DB_PASSWORD=6A2tMvEIUABMc4yuY6Ih
ENV DB_HOST=containers-us-west-23.railway.app
ENV DB_PORT=6297
ENV DB_NAME=railway
ENV SMTP_EMAIL=aupmaan@gmail.com
ENV SMTP_PASSWORD=osutizmswudoiupr
ENV PORT=8000

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application