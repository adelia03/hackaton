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

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application