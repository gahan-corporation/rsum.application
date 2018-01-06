FROM python:alpine3.7
RUN apk update
RUN apk add git postgresql-dev make g++ libxml2-dev libxslt-dev
RUN pip install psycopg2 django git+https://github.com/executive-consultants-of-los-angeles/python-docx.git
ADD rsum /srv/rsum
ADD static /srv/static
