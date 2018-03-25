FROM python:3.6.4
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install \
binutils \
libproj-dev \
gdal-bin \
postgresql-client \
libevent-dev \
nodejs \
build-essential \
cron


RUN mkdir /app
RUN mkdir /app/code
RUN mkdir /app/static
RUN mkdir /app/logs
RUN mkdir /app/media


COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app/code/
WORKDIR /app/code

ADD deploy/gunicorn.conf /gunicorn.conf
ADD deploy/gunicorn.sh /gunicorn.sh
RUN chmod +x /gunicorn.sh
ADD deploy/wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
ADD deploy/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
ADD deploy/django-code-entrypoint.sh /django-code-entrypoint.sh
RUN chmod +x /django-code-entrypoint.sh
